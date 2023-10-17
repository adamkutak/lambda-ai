from typing import Annotated

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from lambda_ai.api_models import CreateToolRequest, LoginRequest
from lambda_ai.database.crud.api_function import (
    create_api_function,
    update_api_function,
)
from lambda_ai.database.crud.db import get_db
from lambda_ai.database.schemas.api_function import APIFunctionCreate
from lambda_ai.database.schemas.user import CreateUser, User
from lambda_ai.database.crud.user import (
    create_user,
    get_user_from_email,
    get_user_from_session,
)
from lambda_ai.lambdaai.apis import APIFunction
from lambda_ai.database.main import db_session
from lambda_ai.lambdaai.db import DB

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
    # how do we define path: user-id + function name?
    fake_user_id = "xyz_123_abc_789"
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
        raise HTTPException(
            status_code=500, detail=f"Failed to build tool successfully: {message}"
        )

    api_function_created = {
        "api_function_created": new_api_function.api_function_created
    }

    with db_session() as session:
        update_api_function(session, api_function_obj.id, api_function_created)

    return {"message": "success"}


@app.post("/create_database")
def create_database(request: None):
    pass


@app.post("/create_table")
def create_table(request: None):
    pass


@app.get("/get_tools")
def get_tools(request: None):
    pass


@app.get("/get_databases")
def get_databases(request: None):
    pass


@app.post("/query_tool")
def query_tool(request: None):
    pass


@app.post("/register")
def register(request: CreateUser):
    # create new user in database
    with db_session() as db:
        new_user = create_user(db=db, user=request)

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


@app.get("/login")
def login(request: LoginRequest, bearer_token: Annotated[str | None, Header()] = None):
    with db_session() as db:
        user = get_user_from_email(db=db, email=LoginRequest.email)

    user_return = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "id": user.id,
    }

    response = JSONResponse(user_return)

    if not bearer_token:
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
