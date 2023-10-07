from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .base import Base
from contextlib import contextmanager
from .models import APIFunctionModel, Table

load_dotenv()
DATABASE_URL = os.environ.get("POSTGRES_DB_URL")
engine = create_engine(DATABASE_URL, echo=False)  # set echo to false for less verbosity
SessionLocal = sessionmaker(bind=engine)
# drop foreign key dependant tables first:
APIFunctionModel.__table__.drop(engine)
Table.__table__.drop(engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@contextmanager
def db_session():
    session = SessionLocal()
    yield session
    session.commit()
    session.close()


@contextmanager
def db_test_session():
    session = SessionLocal()
    session.begin_nested()  # Begin a nested transaction
    yield session
    session.rollback()  # Rollback the session after the test
    session.close()
