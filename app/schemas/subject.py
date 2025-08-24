# from enum import Enum
from pydantic import BaseModel
from datetime import datetime, date


class SubjectBase(BaseModel):
    name: str
    code: str
    created_at: datetime
    updated_at: datetime


class SubjectCreate(SubjectBase):
    pass


class SubjectOut(SubjectBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
