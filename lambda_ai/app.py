import os
import openai
from dotenv import load_dotenv
from typing import Annotated

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from lambda_ai.api_models import (
    CreateTableRequest,
    CreateToolRequest,
    QueryToolRequest,
    LoginRequest,
)

from lambda_ai.database.crud.api_container import (
    create_api_environment,
    create_api_file,
    get_all_api_environments,
    get_api_file,
    update_api_environment,
    update_api_file,
)
from lambda_ai.database.crud.api_function import (
    create_api_function,
    delete_api_function,
    get_api_function,
    get_api_functions,
    update_api_function,
)
from lambda_ai.database.crud.db import create_db, get_all_dbs, get_db
from lambda_ai.database.crud.table import (
    create_table as create_db_table,
    get_all_tables_by_db,
)
from lambda_ai.database.crud.user import (
    create_user,
    get_user_from_email,
    get_user_from_session,
)

from lambda_ai.database.schemas.api_container import APIEnvironmentCreate, APIFileCreate
from lambda_ai.database.schemas.api_function import APIFunctionCreate
from lambda_ai.database.schemas.db import DBCreate
from lambda_ai.database.schemas.table import TableCreate
from lambda_ai.database.schemas.user import CreateUser

from lambda_ai.lambdaai.apis import APIFunction
from lambda_ai.database.main import db_session
from lambda_ai.lambdaai.db import DB, DEFAULT_DB_PATH
from lambda_ai.lambdaai.environment import APIEnvironment, APIFile


from lambda_ai.lambdaai.utils import generate_slug, parse_bearer_token


# running on app startup.
def onstartup():
    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")


onstartup()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_tool")
def create_tool(
    request: CreateToolRequest, authorization: Annotated[str | None, Header()] = None
):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    # FIXME: paths are a mess
    # how do we define path: user-id + function name?
    # Michael: won't pass .isidentifier() with user-int(int) first... supplied a temp fix.
    authed_user_id = authed_user.id
    slug_name = generate_slug(request.tool.name)
    built_path = "user" + str(authed_user_id) + "/" + slug_name

    testcases = [testcase.model_dump() for testcase in request.testcases]

    # create object in database (set api_function_created to empty)
    new_function = APIFunctionCreate(
        name=request.tool.name,
        slug_name=slug_name,
        path=built_path,
        inputs=dict(request.tool.inputs),
        outputs=dict(request.tool.outputs),
        functionality=request.tool.description,
        test_cases=testcases,
        force_use_db=False,
        is_async=False,
        attached_db=request.tool.selectedDatabase,
        user_id=authed_user_id,
    )

    with db_session() as session:
        api_function_obj = create_api_function(session, new_function)
        api_obj_id = api_function_obj.id

    if request.tool.selectedDatabase:
        with db_session() as session:
            db_obj = get_db(session, request.tool.selectedDatabase)
            if db_obj:
                attached_db = DB(name=db_obj.slug_name, location=db_obj.location)
            else:
                print("Attempted to attach a database that was not found")
                return JSONResponse(
                    {"error": "Attempted to attach a database that was not found"},
                    status_code=400,
                )
    else:
        attached_db = None

    # now we try to generate the API function.
    new_api_function = APIFunction(
        name=new_function.slug_name,
        path=built_path,
        inputs=dict(request.tool.inputs),
        outputs=dict(request.tool.outputs),
        functionality=request.tool.description,
        test_cases=testcases,
        force_use_db=False,
        is_async=False,
        attached_db=attached_db,
    )

    result_code, message = new_api_function.create_api_function()
    if result_code > 1:
        print(message)
        with db_session():
            delete_api_function(session, api_obj_id)
        return JSONResponse(
            {"error": f"Failed to build tool: {message}"}, status_code=500
        )

    api_function_created = {
        "api_function_created": new_api_function.api_function_created
    }

    with db_session() as session:
        update_api_function(session, api_obj_id, **api_function_created)

    # the following code is a collosal mess. Will fix this soon.
    # FIXME: for now, we just attach it to the first apienv in the database.
    # We will just have 1 api environment right now. In the future, the user
    # could have collections of tools in the UI, and a collection would be
    # represented by an api-env/api-file.
    # FIXME: we have to get rid of these classes. Pass in schemas instead,
    #        and use the database in the core lambdaai directory.
    with db_session() as session:
        envs = get_all_api_environments(
            session, authed_user_id
        )  # gets only authed users envs
    if envs:
        master_env = envs[0]
        with db_session() as session:
            master_file = get_api_file(session, master_env.api_file_id)
        api_file = APIFile(
            master_file.slug_name,
            master_file.file_path,
            master_file.attach_db or attached_db is not None,
            pulling_old=True,
        )

        new_function_dict = master_file.functions.copy()
        new_function_dict[new_api_function.api_function_created["name"]] = {
            "path": new_api_function.api_function_created["path"],
            "function_code": new_api_function.api_function_created["function_code"],
            "imports": new_api_function.api_function_created["imports"],
        }
        for key, value in new_function_dict.items():
            api_file.add_function(
                {
                    "name": key,
                    "path": value["path"],
                    "function_code": value["function_code"],
                    "imports": value["imports"],
                }
            )
        api_file.black_format_file()

        api_env = APIEnvironment(
            api_file,
            master_env.host,
            master_env.port,
            master_env.is_live,
            server_process_id=master_env.server_process_id,
        )

        if api_env.is_live:
            api_env.undeploy()
        api_env.deploy()

        with db_session() as session:
            update_api_file(session, master_file.id, functions=new_function_dict)
            update_api_environment(session, master_env.id, is_live=True)

    else:
        master_env = None
        api_file = APIFile(
            name="master_env_file",
            file_path="lambda_ai/generated_tools",
            attach_db=attached_db is not None,
        )
        api_file.add_function(new_api_function.api_function_created)
        api_file.black_format_file()

        api_env = APIEnvironment(api_file)
        api_env.deploy()

        transformed_function = {}
        transformed_function[new_api_function.api_function_created["name"]] = {
            "path": new_api_function.api_function_created["path"],
            "function_code": new_api_function.api_function_created["function_code"],
            "imports": new_api_function.api_function_created["imports"],
        }

        api_schema = APIFileCreate(
            name=api_file.name,
            slug_name=generate_slug(api_file.name),
            file_path=api_file.file_path,
            functions=transformed_function,
            attach_db=attached_db is not None,
            user_id=authed_user_id,
        )

        with db_session() as session:
            api_file_obj = create_api_file(session, api_schema)

        env_schema = APIEnvironmentCreate(
            api_file_id=api_file_obj.id,
            file_uvicorn=api_env.file_uvicorn,
            requirements_file=api_env.requirements_file,
            is_live=api_env.is_live,
            server_process_id=api_env.server_process_id,
            user_id=authed_user_id,
        )
        with db_session() as session:
            create_api_environment(session, env_schema)

    new_api_function_return = {
        "id": api_obj_id,
        "name": new_api_function.name,
        "inputs": new_api_function.inputs,
        "outputs": new_api_function.outputs,
        "description": new_api_function.functionality,
    }
    return {"tool": new_api_function_return}


@app.post("/create_database")
def create_database(
    request: CreateTableRequest, authorization: Annotated[str | None, Header()] = None
):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    new_database = DBCreate(
        name=request.name,
        slug_name=generate_slug(request.name),
        location=DEFAULT_DB_PATH,
        user_id=authed_user.id,
    )
    with db_session() as session:
        db_obj = create_db(session, new_database)
        return db_obj.id


@app.post("/create_table")
def create_table(
    request: CreateTableRequest, authorization: Annotated[str | None, Header()] = None
):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    # temporarily call create_database when we want to make a new table
    db_id = create_database(request, authorization)
    with db_session() as session:
        db_obj = get_db(session, db_id)
        db = DB(name=db_obj.slug_name, location=db_obj.location, replace_existing=True)

    # transform the columns because TableCreate takes a dict of columns
    transform_columns = {}
    for column in request.columns:
        transform_column = column.model_dump()
        constraints = []
        if transform_column["primary_key"]:
            constraints.append("primary key")
        if transform_column["unique"]:
            constraints.append("unique")

        transform_columns[transform_column["name"]] = {
            "type": transform_column["type"],
            "constraints": constraints,
        }

    table_create = TableCreate(
        name=request.name,
        slug_name=generate_slug(request.name),
        description=request.description,
        columns=transform_columns,
        db_id=db_id,
    )
    with db_session() as session:
        table_obj = create_db_table(session, table_create)
        db.add_table(table_obj.name, table_obj.columns)

    new_table_return = {
        "id": db_id,  # temporary 1-1 relationship for db-table
        "name": table_obj.name,
        "columns": transform_columns,
        "description": table_obj.description,
    }

    return {"table": new_table_return}


@app.get("/get_tools")
def get_tools(authorization: Annotated[str | None, Header()] = None):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    with db_session() as session:
        tools = get_api_functions(session, authed_user.id)

    tools_list = []
    for tool in tools:
        tools_list.append(
            {
                "id": tool.id,
                "name": tool.name,
                "inputs": tool.inputs,
                "outputs": tool.outputs,
                "description": tool.functionality,
            }
        )

    return {"tools": tools_list}


@app.get("/get_databases")
def get_databases(authorization: Annotated[str | None, Header()] = None):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    with db_session() as session:
        dbs = get_all_dbs(session, authed_user.id)

        dbs_list = []
        for db in dbs:
            tables = get_all_tables_by_db(session, db.id)
            tables_list = [
                {
                    "id": table.id,
                    "name": table.name,
                    "description": table.description,
                    "columns": table.columns,
                }
                for table in tables
            ]
            dbs_list.append(
                {
                    "id": db.id,
                    "name": db.name,
                    "tables": tables_list,
                }
            )

    return {"databases": dbs_list}


# this is a temporary function to get all the tables
# in the future, tables in the UI will be part of a database
@app.get("/get_tables")
def get_tables(authorization: Annotated[str | None, Header()] = None):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    with db_session() as session:
        dbs = get_all_dbs(session, authed_user.id)

        master_tables_list = []
        for db in dbs:
            tables = get_all_tables_by_db(session, db.id)
            tables_list = [
                {
                    "id": db.id,  # temporary 1-1 relation db-table
                    "name": table.name,
                    "description": table.description,
                    "columns": table.columns,
                }
                for table in tables
            ]
            master_tables_list.extend(tables_list)

    return {"tables": master_tables_list}


@app.post("/query_tool")
def query_tool(
    request: QueryToolRequest, authorization: Annotated[str | None, Header()] = None
):
    session_id = parse_bearer_token(authorization)

    with db_session() as db:
        authed_user = get_user_from_session(db, session_id)

    if not authed_user:
        return JSONResponse(
            {"error": "Authentication credentials invalid."}, status_code=400
        )

    with db_session() as session:
        envs = get_all_api_environments(session, authed_user.id)

        if not envs:
            return JSONResponse({"error": "No tools to query."}, status_code=400)

        # REVIEW: Not using master env anymore bcuz getting only user owned envs.
        # But, doesn't matter what env is used... can query any tool from
        # any API as long as tool is live. If user owns no envs, they haven't deployed
        # any tools so we can return error.
        first_env_found = envs[0]
        first_file_found = get_api_file(session, first_env_found.api_file_id)

    # FIXME: the following code is awful. This is a dummy api_file that
    # we have to create so that we can instantiate the APIEnv.
    api_file = APIFile(
        first_file_found.slug_name,
        first_file_found.file_path,
        first_file_found.attach_db,
        pulling_old=True,
    )
    api_env = APIEnvironment(
        api_file, first_env_found.host, first_env_found.port, first_env_found.is_live
    )

    with db_session() as session:
        tool = get_api_function(session, request.id, authed_user.id)

    if not tool:
        return {"error": "Unable to query requested tool."}

    e, response = api_env.query(tool.path, request.inputs)

    if not e:
        return {"output": response.json()}
    else:
        return {"error": e}


@app.post("/register")
def register(request: CreateUser):
    # create new user in database
    try:
        with db_session() as db:
            new_user = create_user(db=db, user=request)

    except Exception:
        return JSONResponse({"error": "Email alrady in use."}, status_code=400)

    new_user_return = {
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "id": new_user.id,
    }

    response = JSONResponse(new_user_return)

    # Pass back session ID as a cookie for browser to store
    session_id = new_user.session_id
    response.set_cookie(  # TODO: Add safety params for prod environment
        key="session_id",
        value=session_id,
        path="/",
        # secure=True,
        # httponly=True,
        # samesite='strict'
    )

    return response


# FIXME: Code is kinda ugly, probs could be redone better. Later.
# NOTE: If logging in with bearer token, must send LoginRequest with blank email and pass fields.
@app.get("/login")
def login(request: LoginRequest, authorization: Annotated[str | None, Header()] = None):
    user = None

    if authorization:
        session_id = parse_bearer_token(authorization)

        with db_session() as db:
            user = get_user_from_session(db, session_id)

    if not user:
        with db_session() as db:
            user = get_user_from_email(db=db, email=request.email)

        if not user:
            return JSONResponse(
                {"error": "Incorrect username and password"}, status_code=400
            )

    user_return = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "id": user.id,
    }

    response = JSONResponse(user_return)

    if not authorization:
        session_id = user.session_id
        response.set_cookie(  # TODO: Add safety params for prod environment
            key="session_id",
            value=session_id,
            path="/",
            # secure=True,
            # httponly=True,
            # samesite='strict'
        )

    return response
