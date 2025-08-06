from pydantic import BaseModel, EmailStr


class ResultBase(BaseModel):
    student_id: int
    subject_id: int
    term: str
    year_id: int
    score: float


class ResultCreate(ResultBase):
    pass


class ResultOut(ResultBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}


class ResultUpdate(BaseModel):
    score: float
