# from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    gender: str
    fee_status: str
    date_of_birth: datetime  # ISO date string
    guardian_name: Optional[str] = None
    guardian_contact: Optional[str] = None
    address: Optional[str] = None


class StudentCreate(StudentBase):
    class_id: int  # link to a Class


class StudentOut(StudentBase):
    id: int
    class_id: int
    class_name: str  # 💡 Not in DB directly — must come from JOIN
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
