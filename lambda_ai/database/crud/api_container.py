from sqlalchemy.orm import Session
from database.models.api_container import APIEnvironmentModel, APIFileModel
from database.schemas.api_container import (
    APIEnvironment,
    APIEnvironmentCreate,
    APIFile,
    APIFileCreate,
)


def create_api_file(db: Session, file_data: APIFileCreate):
    file_obj = APIFileModel(**file_data.model_dump())
    db.add(file_obj)
    db.commit()
    db.refresh(file_obj)
    return file_obj


def get_api_file(db: Session, file_id: int):
    file_obj = db.query(APIFileModel).filter(APIFileModel.id == file_id).first()
    return file_obj


def get_all_api_files(db: Session, skip: int = 0, limit: int = 100) -> list[APIFile]:
    file_objs = db.query(APIFileModel).offset(skip).limit(limit).all()
    return [file for file in file_objs]


def delete_api_file(db: Session, file_id: int):
    file_obj = db.query(APIFileModel).filter(APIFileModel.id == file_id).first()
    db.delete(file_obj)
    db.commit()


def update_api_file(db: Session, file_id: int, **kwargs):
    db_file = db.query(APIFileModel).filter(APIFileModel.id == file_id).first()

    if not db_file:
        return None

    for key, value in kwargs.items():
        if hasattr(db_file, key):
            setattr(db_file, key, value)

    db.commit()
    db.refresh(db_file)

    return db_file


def create_api_environment(db: Session, env_data: APIEnvironmentCreate):
    env_obj = APIEnvironmentModel(**env_data.model_dump())
    db.add(env_obj)
    db.commit()
    db.refresh(env_obj)
    return env_obj


def get_api_environment(db: Session, env_id: int):
    env_obj = (
        db.query(APIEnvironmentModel).filter(APIEnvironmentModel.id == env_id).first()
    )
    return env_obj


def get_all_api_environments(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[APIEnvironment]:
    env_objs = (
        db.query(APIEnvironmentModel)
        .filter(APIEnvironmentModel.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [env for env in env_objs]


def delete_api_environment(db: Session, env_id: int):
    env_obj = (
        db.query(APIEnvironmentModel).filter(APIEnvironmentModel.id == env_id).first()
    )
    db.delete(env_obj)
    db.commit()


def update_api_environment(db: Session, env_id: int, **kwargs):
    db_env = (
        db.query(APIEnvironmentModel).filter(APIEnvironmentModel.id == env_id).first()
    )

    if not db_env:
        return None

    for key, value in kwargs.items():
        if hasattr(db_env, key):
            setattr(db_env, key, value)

    db.commit()
    db.refresh(db_env)

    return db_env
