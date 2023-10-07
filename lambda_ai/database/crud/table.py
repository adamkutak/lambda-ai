from sqlalchemy.orm import Session
from lambda_ai.database.models.table import Table
from lambda_ai.database.schemas.table import TableCreate

def create_table(db: Session, table_data: TableCreate):
    table_obj = Table(**table_data.model_dump())
    db.add(table_obj)
    db.commit()
    db.refresh(table_obj)
    return table_obj

def get_table(db: Session, table_id: int):
    table_obj = db.query(Table).filter(Table.id == table_id).first()
    return table_obj

def get_all_tables_by_db(db: Session, db_id: int):
    table_obj = db.query(Table).filter(Table.db_id == db_id).all()
    return table_obj

def delete_table(db: Session, table_id: int):
    table_obj = db.query(Table).filter(Table.id == table_id).first()
    db.delete(table_obj)
    db.commit()

    return table_obj