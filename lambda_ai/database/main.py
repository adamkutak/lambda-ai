from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .base import Base
from . import models

load_dotenv()
DATABASE_URL = os.environ.get("POSTGRES_DB_URL")
engine = create_engine(DATABASE_URL, echo=False) # set echo to false for less verbosity
SessionLocal = sessionmaker(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
