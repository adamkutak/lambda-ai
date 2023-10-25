from pydantic import BaseModel
from typing import Optional

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8005"


class APIEnvironmentBase(BaseModel):
    api_file_id: int
    host: str = DEFAULT_HOST
    port: str = DEFAULT_PORT
    file_uvicorn: str
    requirements_file: str
    is_live: Optional[bool] = False
    server_process_id: Optional[int] = None
    user_id: int


class APIEnvironmentCreate(APIEnvironmentBase):
    pass


class APIEnvironment(APIEnvironmentBase):
    id: int


class APIFileBase(BaseModel):
    name: str
    slug_name: str
    file_path: str
    functions: dict = {}
    attach_db: bool = False
    user_id: int


class APIFileCreate(APIFileBase):
    pass


class APIFile(APIFileBase):
    id: int
