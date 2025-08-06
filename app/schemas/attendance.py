from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import List, Optional

from app.models.enums import AttendanceStatusEnum


class AttendanceRecord(BaseModel):
    student_id: int
    status: AttendanceStatusEnum
    note: Optional[str] = None


class AttendanceCreate(BaseModel):
    class_id: int
    academic_year_id: int
    date: date
    marked_by: Optional[int] = None
    records: List[AttendanceRecord]


class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatusEnum] = None
    remark: Optional[str] = None


class AttendanceOut(BaseModel):
    id: int
    student_id: int
    class_id: int
    academic_year_id: int
    date: date
    status: AttendanceStatusEnum
    marked_by: Optional[int] = None
    remark: Optional[str] = None

    class Config:
        model_config = {"from_attributes": True}


class AttendanceHistoryOut(BaseModel):
    id: int
    date: date
    student_name: str
    class_name: str
    status: AttendanceStatusEnum
    note: str | None = None
    marked_by: str | None = None  # Name of the teacher/user who marked it

    class Config:
        model_config = {"from_attributes": True}
