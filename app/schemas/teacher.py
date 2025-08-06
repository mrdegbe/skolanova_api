# from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from app.schemas.class_ import HomeroomClassOut
from app.schemas.class_subject_teacher import ClassSubjectTeacherOut


class Assignment(BaseModel):
    class_id: int
    subject_ids: List[int]


class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    email: EmailStr
    contact: str
    status: str
    address: Optional[str] = None
    specialization: str
    assignments: Optional[List[Assignment]] = []


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    status: Optional[str] = None
    specialization: Optional[str] = None
    address: Optional[str] = None
    assignments: Optional[List[Assignment]] = []

    class Config:
        model_config = {"from_attributes": True}


# DB + internal use
class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    user_id: int


class TeacherResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        model_config = {"from_attributes": True}


class TeacherOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender: str
    email: str
    contact: str
    status: str
    specialization: Optional[str]
    address: Optional[str]
    homeroom_classes: List[HomeroomClassOut]
    created_at: datetime
    updated_at: datetime
    subject_links: List[ClassSubjectTeacherOut] = []

    class Config:
        model_config = {"from_attributes": True}
