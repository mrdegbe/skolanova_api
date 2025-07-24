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

    class Config:
        orm_mode = True
