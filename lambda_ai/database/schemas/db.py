from pydantic import BaseModel


class DBBase(BaseModel):
    name: str
    slug_name: str
    location: str
    user_id: int


class DBCreate(DBBase):
    pass


class DB(DBBase):
    id: int
