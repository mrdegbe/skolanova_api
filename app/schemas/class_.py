# from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

from app.models.academic_year import AcademicYear


class ClassBase(BaseModel):
    name: str
    class_teacher_id: Optional[int] = None  # ✅ allow NULLs
    academic_year_id: int  # Now required!


class ClassCreate(ClassBase):
    pass


class Class(ClassBase):
    id: int
    academic_year: AcademicYear  # Embedded

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }


class ClassOut(BaseModel):
    id: int
    name: str
    class_teacher_id: Optional[int] = None
    class_teacher_name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ClassUpdate(BaseModel):
    name: Optional[str] = None
    class_teacher_id: Optional[int] = None
