from pydantic import BaseModel
from typing import List, Dict, Optional

class APIFunctionBase(BaseModel):
    name: str
    path: str
    inputs: Dict
    outputs: Dict
    functionality: str
    test_cases: List[Dict]
    is_async: Optional[bool] = False
    build_attempts: List[Dict] = []
    api_function_created: Dict = {}
    attached_db_id: Optional[int] = None
    force_use_db: bool

class APIFunctionCreate(APIFunctionBase):
    pass

class APIFunction(APIFunctionBase):
    id: int
