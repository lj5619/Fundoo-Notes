from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    notes = relationship("Note", back_populates="user", cascade="all, delete")
    labels = relationship("Label", back_populates="user", cascade="all, delete")
