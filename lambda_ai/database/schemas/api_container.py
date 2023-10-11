from pydantic import BaseModel
from typing import Optional
from lambda_ai.lambdaai.environment import DEFAULT_HOST, DEFAULT_PORT


class APIEnvironmentBase(BaseModel):
    api_file_id: int
    host: str = DEFAULT_HOST
    port: str = DEFAULT_PORT
    file_uvicorn: str
    requirements_file: str
    is_live: Optional[bool] = False
    server_process_id: Optional[int] = None


class APIEnvironmentCreate(APIEnvironmentBase):
    pass


class APIEnvironment(APIEnvironmentBase):
    id: int


class APIFileBase(BaseModel):
    name: str
    file_path: str
    functions: dict = {}
    attach_db: bool = False


class APIFileCreate(APIFileBase):
    pass


class APIFile(APIFileBase):
    id: int
