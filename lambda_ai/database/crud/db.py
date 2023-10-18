from sqlalchemy.orm import Session
from lambda_ai.database.models.api_function import APIFunctionModel
from lambda_ai.database.models.db import DBModel
from lambda_ai.database.schemas.db import DBCreate


def create_db(db: Session, db_data: DBCreate):
    db_obj = DBModel(name=db_data.name, location=db_data.location)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_db(db: Session, db_id: int):
    db_obj = db.query(DBModel).filter(DBModel.id == db_id).first()
    return db_obj


def get_all_dbs(db: Session, skip: int = 0, limit: int = 100):
    db_obj = db.query(DBModel).offset(skip).limit(limit).all()
    return db_obj


def delete_db(db: Session, db_id: int):
    # delete associated api functions
    apis_with_attached_db = (
        db.query(APIFunctionModel)
        .filter(APIFunctionModel.attached_db_id == db_id)
        .all()
    )
    for api in apis_with_attached_db:
        db.delete(api)

    db_obj = db.query(DBModel).filter(DBModel.id == db_id).first()
    db.delete(db_obj)
    db.commit()

    return db_obj
