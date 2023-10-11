from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import CreateUser, User


def create_user(db: Session, user: CreateUser):
    # create a user
    new_user = UserModel(**user.model_dump())

    # insert into database
    db.add(new_user)

    # commit & refresh
    db.commit()
    db.refresh(new_user)

    return new_user


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
