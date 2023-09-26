from pydantic import BaseModel


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8000"

class APIEnvironmentBase(BaseModel):
    api_file_id: int
    host: str = DEFAULT_HOST
    port: str = DEFAULT_PORT
    file_uvicorn: str
    requirements_file: str

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