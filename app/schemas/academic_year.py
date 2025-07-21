# from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date


# ----- Acasemic Year -----
class AcademicYearBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_active: Optional[bool] = True


class AcademicYearCreate(AcademicYearBase):
    pass


class AcademicYear(AcademicYearBase):
    id: int

    class Config:
        orm_mode = True


# I believe it's same concept as academic year

# class YearBase(BaseModel):
#     year: int


# class YearCreate(YearBase):
#     pass


# class YearOut(YearBase):
#     id: int

#     class Config:
#         orm_mode = True
