# from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date


class AcademicYearBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_active: Optional[bool] = True


class AcademicYearCreate(AcademicYearBase):
    pass


class AcademicYear(AcademicYearBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
