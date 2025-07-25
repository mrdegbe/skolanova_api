from pydantic import BaseModel, EmailStr


class RemarkBase(BaseModel):
    result_id: int
    teacher_id: int
    comment: str


class RemarkCreate(RemarkBase):
    pass


class RemarkOut(RemarkBase):
    id: int

    class Config:
        orm_mode = True
