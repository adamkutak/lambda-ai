from sqlalchemy.orm import Session
from lambda_ai.database.models.user import UserModel
from lambda_ai.database.schemas.user import CreateUser, User
from lambda_ai.lambdaai.utils import unsafe_session_id


def create_user(db: Session, user: CreateUser):
    # generate session ID
    session_id = unsafe_session_id(user.first_name)  # TODO: Update with safe session ID

    # create a user
    new_user = UserModel(**user.model_dump(), session_id=session_id)

    # insert into database
    db.add(new_user)

    # commit & refresh
    # db.commit()
    # db.refresh(new_user)

    return new_user


def get_user_from_session(db: Session, session_id: str):
    user = db.query(UserModel).filter(UserModel.session_id == session_id).first()

    return user


def get_user_from_email(db: Session, email: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    return user


def get_user(db: Session, user_id: int) -> User:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    users = db.query(UserModel).offset(skip).limit(limit).all()

    return users


def update_user(db: Session, user_id: int, **kwargs):
    user = db.query(UserModel).get(user_id)

    if not user:
        return None

    for key, value in kwargs:
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(UserModel).get(user_id)

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True
