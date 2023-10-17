from pydantic import BaseModel


class TableBase(BaseModel):
    name: str
    slug_name: str
    description: str
    columns: dict
    db_id: int


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int
