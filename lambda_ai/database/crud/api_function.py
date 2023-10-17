from sqlalchemy.orm import Session
from lambda_ai.database.models.api_function import APIFunctionModel
from lambda_ai.database.schemas.api_function import APIFunctionCreate


def create_api_function(db: Session, api_function: APIFunctionCreate):
    db_api_function = APIFunctionModel(**api_function.model_dump())
    db.add(db_api_function)
    db.commit()
    db.refresh(db_api_function)

    return db_api_function


def get_api_function(db: Session, api_function_id: int):
    db_api_function = (
        db.query(APIFunctionModel)
        .filter(APIFunctionModel.id == api_function_id)
        .first()
    )

    return db_api_function


def get_api_functions(db: Session, skip: int = 0, limit: int = 100):
    db_api_function = db.query(APIFunctionModel).offset(skip).limit(limit).all()

    return db_api_function


def update_api_function(db: Session, api_function_id: int, **kwargs):
    db_api_function = (
        db.query(APIFunctionModel)
        .filter(APIFunctionModel.id == api_function_id)
        .first()
    )

    if not db_api_function:
        return None

    for key, value in kwargs.items():
        if hasattr(db_api_function, key):
            setattr(db_api_function, key, value)

    db.commit()
    db.refresh(db_api_function)

    return db_api_function


def delete_api_function(db: Session, api_function_id: int):
    table_obj = (
        db.query(APIFunctionModel)
        .filter(APIFunctionModel.id == api_function_id)
        .first()
    )
    db.delete(table_obj)
    db.commit()

    return table_obj
