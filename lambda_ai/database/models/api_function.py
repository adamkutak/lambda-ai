from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from lambda_ai.database.base import Base


class APIFunctionModel(Base):
    __tablename__ = "api_functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    slug_name = Column(String, unique=True, index=True)
    path = Column(String, unique=True, index=True)
    inputs = Column(JSON)
    outputs = Column(JSON)
    functionality = Column(String)
    test_cases = Column(JSON)
    is_async = Column(Boolean)
    build_attempts = Column(JSON, default=[])
    api_function_created = Column(JSON, default={})
    attached_db_id = Column(Integer, ForeignKey("databases.id"), nullable=True)
    force_use_db = Column(Boolean)

    model_config = ConfigDict(from_attributes=True)
