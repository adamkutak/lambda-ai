from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from lambda_ai.database.base import Base


class TableModel(Base):
    __tablename__ = "db_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    columns = Column(JSON)
    db_id = Column(Integer, ForeignKey("databases.id"), nullable=True)
