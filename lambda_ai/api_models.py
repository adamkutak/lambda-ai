import json
from typing import List, Any, Dict, Optional
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    inputs: Dict[str, str]
    outputs: Dict[str, str]
    description: str
    selectedDatabase: Optional[int] = None


class TestCase(BaseModel):
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]


class CreateToolRequest(BaseModel):
    tool: Tool
    testcases: List[TestCase]


# print(json.dumps(CreateToolRequest.model_json_schema(), indent=2))
