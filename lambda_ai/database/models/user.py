from sqlalchemy import Column, Integer, String
from lambda_ai.database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, default="")
    last_name = Column(String, index=True, default="")
    email = Column(String, unique=True, index=True)
    password = Column(String)
    session_id = Column(String(128), unique=True, nullable=False)
