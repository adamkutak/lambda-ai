from sqlalchemy.orm import Session
from lambda_ai.database.models.db import DBModel
from lambda_ai.database.schemas.db import DBCreate


def create_db(db: Session, db_data: DBCreate):
    db_obj = DBModel(**db_data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_db(db: Session, db_id: int, user_id: int):
    db_obj = (
        db.query(DBModel)
        .filter(DBModel.id == db_id)
        .filter(DBModel.user_id == user_id)
        .first()
    )
    return db_obj


def get_all_dbs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    db_obj = (
        db.query(DBModel)
        .filter(DBModel.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return db_obj


def delete_db(db: Session, db_id: int):
    db_obj = db.query(DBModel).filter(DBModel.id == db_id).first()
    db.delete(db_obj)
    db.commit()

    return db_obj
