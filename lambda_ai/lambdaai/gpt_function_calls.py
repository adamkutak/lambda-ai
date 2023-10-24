from pydantic import BaseModel, Field
from typing import Any, List

# FUNCTION_CALLING_ENDPOINT_CREATION = {
#     "name": "create_api",
#     "description": "Create a new API endpoint and test it. If an error occurs during testing, the error will be returned to you.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "imports": {
#                 "type": "string",
#                 "description": "the python code to import the necessary requirements.",
#             },
#             "endpoint": {
#                 "type": "string",
#                 "description": "the python code for your FastAPI endpoint. It must include the decorator and function definition",
#             },
#         },
#         "required": ["imports", "endpoint"],
#     },
# }


# FUNCTION_CALLING_TEST_CREATION = {
#     "name": "add_test",
#     "description": "Create a new test case to be run on a FastAPI endpoint",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "input": {
#                 "type": "object",
#                 "description": "The test inputs. They should match the inputs of the endpoint described.",
#             },
#             "output": {
#                 "type": "object",
#                 "description": "The test outputs. Make sure they match the output types of the function description.",
#             },
#         },
#         "required": ["input", "output"],
#     },
# }


# FUNCTION_CALLING_TEST_CREATION_DB_EXT = {
#     "name": "add_test",
#     "description": "Create a new test case to be run on a FastAPI endpoint",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "input": {
#                 "type": "object",
#                 "description": "The test inputs. They should match the inputs of the endpoint described.",
#             },
#             "output": {
#                 "type": "object",
#                 "description": "The test outputs. Make sure they match the output types of the function description.",
#             },
#             "pre_sql": {
#                 "type": "array",
#                 "description": "A list of str, where each str is a valid SQL you wish to run before the function is tested.",
#             },
#             "post_sql": {
#                 "type": "array",
#                 "description": "A list of dicts, where each dict has two keys: sql, the sql to run to check the database after the test, and assert_value which is the value you expect your sql to return if the test is successful.",
#             },
#         },
#         "required": ["input", "output", "pre_sql", "post_sql"],
#     },
# }


class EndpointCreation(BaseModel):
    imports: str = Field(
        ...,
        description="the python code to import the necessary requirements.",
    )
    endpoint: str = Field(
        ...,
        description="the python code for your FastAPI endpoint. It must include the decorator and function definition",
    )


class EndpointCreation(BaseModel):
    imports: str = Field(
        ...,
        description="the python code to import the necessary requirements.",
    )
    endpoint: str = Field(
        ...,
        description="the python code for your FastAPI endpoint. It must include the decorator and function definition",
    )


class PostSql(BaseModel):
    sql: str = Field(
        ...,
        description="the sql to run to check the database after the test",
    )
    assert_value: Any = Field(
        ...,
        description="the value you expect your sql to return if the test is successful.",
    )


class FunctionCallTest(BaseModel):
    inputs: dict = Field(
        ...,
        description="The test inputs. They should match the inputs of the endpoint described.",
    )
    outputs: dict = Field(
        ...,
        description="The test outputs. Make sure they match the output types of the function description.",
    )


class FunctionCallTestWithDB(FunctionCallTest):
    pre_sql: List[str] = Field(
        ...,
        description="A list of valid SQL statements. Each is a valid SQL you wish to run before the function is tested.",
    )
    post_sql: List[PostSql] = Field(
        ...,
        description="list of the SQL checks you would want to run to verify the endpoint worked correctly.",
    )


class SQLGeneration(BaseModel):
    pre_sql: List[str] = Field(
        ...,
        description="A list of valid SQL statements. Each is a valid SQL you wish to run before the function is tested.",
    )
    post_sql: List[PostSql] = Field(
        ...,
        description="list of the SQL checks you would want to run to verify the endpoint updated the attached database correctly.",
    )


FUNCTION_CALLING_ENDPOINT_CREATION = {
    "name": "create_api",
    "description": "Create a new API endpoint and test it. If an error occurs during testing, the error will be returned to you.",
    "parameters": EndpointCreation.model_json_schema(),
}

FUNCTION_CALLING_TEST_CREATION = {
    "name": "add_test",
    "description": "Create a new test case to be run on a FastAPI endpoint",
    "parameters": FunctionCallTest.model_json_schema(),
}

FUNCTION_CALLING_TEST_CREATION_DB_EXT = {
    "name": "add_test",
    "description": "Create a new test case to be run on a FastAPI endpoint",
    "parameters": FunctionCallTestWithDB.model_json_schema(),
}

FUNCTION_CALLING_SQL_GENERATION = {
    "name": "create_sql",
    "description": "Create SQL statements to setup a database for testing and to verify that a database was updated correctly after testing.",
    "parameters": SQLGeneration.model_json_schema(),
}
