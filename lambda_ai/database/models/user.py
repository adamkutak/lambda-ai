from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, default="")
    last_name = Column(String, index=True, default="")
    email = Column(String, unique=True, index=True)
    password = Column(String)
    session_id = Column(String(128), unique=True, nullable=False)
    prompt_token_usage = Column(Integer, default=0)
    completion_token_usage = Column(Integer, default=0)

    # relationships
    databases = relationship("DBModel", back_populates="owner")
    api_functions = relationship("APIFunctionModel", back_populates="owner")
