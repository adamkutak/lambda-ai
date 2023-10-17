from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    email: str
    password: str


class CreateUser(UserBase):
    pass


class User(UserBase):
    id: int
    session_id: str
