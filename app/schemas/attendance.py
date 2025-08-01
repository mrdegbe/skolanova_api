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
        orm_mode = True
