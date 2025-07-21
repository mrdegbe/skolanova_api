from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Date,
    Enum,
    func,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum))
    name = Column(String)  # ✅ NEW

    # ✅ Relationships
    teacher = relationship("Teacher", back_populates="user", uselist=False)


# Pydantic schemas ->  [For validation]

# from enum import Enum
# from pydantic import BaseModel, EmailStr
# from typing import Optional, List
# from datetime import datetime, date

# ✅ Role enum to match your models.py
# class RoleEnum(str, Enum):
#     admin = "admin"
#     teacher = "teacher"


# ✅ Request body for creating a user
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str  # Plain text from client
#     role: RoleEnum


# ✅ Response body for reading a user (optional, good for docs)
# class UserRead(BaseModel):
#     id: int
#     email: EmailStr
#     role: RoleEnum

#     class Config:
#         orm_mode = True

# ==== AUTH ====
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


# class UserUpdate(BaseModel):
#     name: str


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     id: int | None = None
