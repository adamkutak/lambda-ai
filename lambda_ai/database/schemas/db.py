from pydantic import BaseModel


class DBBase(BaseModel):
    name: str
    slug_name: str
    location: str


class DBCreate(DBBase):
    pass


class DB(DBBase):
    id: int
