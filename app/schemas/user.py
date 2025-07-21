from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
