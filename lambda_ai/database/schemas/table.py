from pydantic import BaseModel

class TableBase(BaseModel):
    name: str
    columns: dict
    db_id: int

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int
