from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lambda_ai.database.base import Base


class DBModel(Base):
    __tablename__ = "databases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    slug_name = Column(String, unique=True, index=True)
    location = Column(String)

    # relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="databases")

    model_config = ConfigDict(from_attributes=True)
