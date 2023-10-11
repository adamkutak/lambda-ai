from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from lambda_ai.database.base import Base


class APIFileModel(Base):
    __tablename__ = "api_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    file_path = Column(String, unique=True, index=True)
    functions = Column(JSON, default={})
    attach_db = Column(Boolean, default=False)


class APIEnvironmentModel(Base):
    __tablename__ = "api_environments"

    id = Column(Integer, primary_key=True, index=True)
    api_file_id = Column(Integer, ForeignKey("api_files.id"))
    host = Column(String)
    port = Column(String)
    file_uvicorn = Column(String)
    requirements_file = Column(String)
    is_live = Column(Boolean, default=False)
    server_process_id = Column(Integer, default=None)
