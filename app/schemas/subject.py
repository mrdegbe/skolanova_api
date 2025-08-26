# from enum import Enum
from pydantic import BaseModel
from datetime import datetime, date


class SubjectBase(BaseModel):
    name: str
    code: str


class SubjectCreate(SubjectBase):
    pass


class SubjectOut(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}
