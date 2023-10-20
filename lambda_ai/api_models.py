import json
from typing import List, Any, Dict, Optional
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    inputs: Dict[str, str]
    outputs: Dict[str, str]
    description: str
    selectedDatabase: Optional[int] = None


class PostSQL(BaseModel):
    sql: str
    assert_value: str


class TestCaseSQLCheck(BaseModel):
    pre_sql: List[str]
    post_sql: List[PostSQL]


class TestCase(BaseModel):
    input: Dict[str, Any]
    output: Dict[str, Any]
    sqltest: Optional[TestCaseSQLCheck] = None


class CreateToolRequest(BaseModel):
    tool: Tool
    testcases: List[TestCase]


class TableColumns(BaseModel):
    name: str
    type: str
    primary_key: Optional[bool] = False
    unique: Optional[bool] = False


class CreateTableRequest(BaseModel):
    name: str
    description: str
    columns: List[TableColumns]


class QueryToolRequest(BaseModel):
    id: int
    inputs: dict


class LoginRequest(BaseModel):
    email: str
    password: str

      
class DeleteToolRequest(BaseModel):
    id: int

      
class DeleteDatabaseRequest(BaseModel):
    id: int



# print(json.dumps(CreateToolRequest.model_json_schema(), indent=2))
