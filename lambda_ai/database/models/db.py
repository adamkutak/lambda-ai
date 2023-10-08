from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String
from lambda_ai.database.base import Base


class DBModel(Base):
    __tablename__ = "databases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)

    model_config = ConfigDict(from_attributes=True)
