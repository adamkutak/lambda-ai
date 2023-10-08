from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from lambda_ai.api_models import CreateToolRequest
from lambda_ai.database.crud.api_function import (
    create_api_function,
    update_api_function,
)
from lambda_ai.database.crud.db import get_db
from lambda_ai.database.schemas.api_function import APIFunctionCreate
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
