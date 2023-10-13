import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from lambda_ai.api_models import CreateTableRequest, CreateToolRequest, QueryToolRequest
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
from lambda_ai.database.schemas.api_container import APIEnvironmentCreate, APIFileCreate
from lambda_ai.database.schemas.api_function import APIFunctionCreate
from lambda_ai.database.schemas.db import DBCreate
from lambda_ai.database.schemas.table import TableCreate
from lambda_ai.lambdaai.apis import APIFunction
from lambda_ai.database.main import db_session
from lambda_ai.lambdaai.db import DB, DEFAULT_DB_PATH
from lambda_ai.database.crud.table import (
    create_table as create_db_table,
    get_all_tables_by_db,
)
from lambda_ai.lambdaai.environment import APIEnvironment, APIFile
from dotenv import load_dotenv
import openai


# this function is for running things on app startup.
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
def create_tool(request: CreateToolRequest):
    breakpoint()
    # FIXME: paths are a mess
    # how do we define path: user-id + function name?
    fake_user_id = "/xyz_123_abc_789"
    built_path = fake_user_id + "/" + request.tool.name

    testcases = [testcase.model_dump() for testcase in request.testcases]

    # create object in database (set api_function_created to empty)
    new_function = APIFunctionCreate(
        name=request.tool.name,
        path=built_path,
        inputs=dict(request.tool.inputs),
        outputs=dict(request.tool.outputs),
        functionality=request.tool.description,
        test_cases=testcases,
        force_use_db=False,
        is_async=False,
        attached_db=request.tool.selectedDatabase,
    )

    with db_session() as session:
        api_function_obj = create_api_function(session, new_function)
        api_obj_id = api_function_obj.id

    if request.tool.selectedDatabase:
        with db_session() as session:
            db_obj = get_db(session, request.tool.selectedDatabase)
            if db_obj:
                attached_db = DB(name=db_obj.name, location=db_obj.location)
            else:
                print("Attempted to attach a database that was not found")
                raise HTTPException(
                    status_code=500,
                    detail="Attempted to attach a database that was not found",
                )
    else:
        attached_db = None

    # now we try to generate the API function.
    new_api_function = APIFunction(
        name=request.tool.name,
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
        raise HTTPException(status_code=500, detail=f"Failed to build tool: {message}")

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
        envs = get_all_api_environments(session)
    if envs:
        master_env = envs[0]
        with db_session() as session:
            master_file = get_api_file(session, master_env.api_file_id)
        api_file = APIFile(
            master_file.name,
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
            file_path=api_file.file_path,
            functions=transformed_function,
            attach_db=attached_db is not None,
        )

        with db_session() as session:
            api_file_obj = create_api_file(session, api_schema)

        env_schema = APIEnvironmentCreate(
            api_file_id=api_file_obj.id,
            file_uvicorn=api_env.file_uvicorn,
            requirements_file=api_env.requirements_file,
            is_live=api_env.is_live,
            server_process_id=api_env.server_process_id,
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
def create_database(request: CreateTableRequest):
    new_database = DBCreate(name=request.name, location=DEFAULT_DB_PATH)
    with db_session() as session:
        db_obj = create_db(session, new_database)
        return db_obj.id


@app.post("/create_table")
def create_table(request: CreateTableRequest):
    # temporarily call create_database when we want to make a new table
    db_id = create_database(request)
    with db_session() as session:
        db_obj = get_db(session, db_id)
        db = DB(name=db_obj.name, location=db_obj.location, replace_existing=True)

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
def get_tools():
    with db_session() as session:
        tools = get_api_functions(session)

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
def get_databases():
    with db_session() as session:
        dbs = get_all_dbs(session)

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
def get_tables():
    with db_session() as session:
        dbs = get_all_dbs(session)

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
def query_tool(request: QueryToolRequest):
    with db_session() as session:
        envs = get_all_api_environments(session)
        master_env = envs[0]
        master_file = get_api_file(session, master_env.api_file_id)
    # FIXME: the following code is awful. This is a dummy api_file that
    # we have to create so that we can instantiate the APIEnv.
    api_file = APIFile(
        master_file.name, master_file.file_path, master_file.attach_db, pulling_old=True
    )
    api_env = APIEnvironment(
        api_file, master_env.host, master_env.port, master_env.is_live
    )

    with db_session() as session:
        tool = get_api_function(session, request.id)

    e, response = api_env.query(tool.path, request.inputs)

    if not e:
        return {"output": response.json()}
    else:
        return {"error": e}
