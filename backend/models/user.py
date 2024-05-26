from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Add a new column for user ID
    username = Column(String(50), unique=True)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    disabled = Column(Boolean)