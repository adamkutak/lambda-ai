import datetime
from sqlalchemy.orm import Session
from database.models.user import UserModel
from database.schemas.user import CreateUser, User
import hashlib
from datetime import datetime


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


def login_user_with_email_password(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if user and user.password == password:
        return user
    else:
        return None


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

    for key, value in kwargs.items():
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


def unsafe_session_id(rand_str: str):
    date = datetime.now()
    timestamp_str = str(datetime.timestamp(date))

    data = (timestamp_str + rand_str).encode()
    hash = hashlib.sha256(data).hexdigest()

    return hash
