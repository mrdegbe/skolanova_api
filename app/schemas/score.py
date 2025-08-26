# app/schemas/score.py

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List

# from sqlalchemy import UUID


class ScoreBase(BaseModel):
    student_id: int = Field(..., description="ID of the student")
    subject_id: int = Field(..., description="ID of the subject")
    class_score: float = Field(..., ge=0, le=30, description="Class score (0–30)")
    exam_score: float = Field(..., ge=0, le=70, description="Exam score (0–70)")
    term: str = Field(..., description="Term (e.g. 'Term 1', 'Term 2', 'Term 3')")
    academic_year_id: int = Field(..., description="ID of the Academic year")


from pydantic import BaseModel
from typing import List


class ScoreRecord(BaseModel):
    student_id: int
    class_score: int
    exam_score: int


class ScoreCreatePayload(BaseModel):
    class_id: int
    subject_id: int
    academic_year_id: int
    term: str
    records: List[ScoreRecord]


# class ScoreOut(ScoreBase):
#     """Schema for returning a score entry"""

#     id: int = Field(..., description="ID of the score entry")


class ScoreOut(BaseModel):
    id: UUID
    student_id: int
    subject_id: int
    class_id: int
    term: str
    academic_year_id: int
    class_score: float
    exam_score: float
    total_score: Optional[float] = None
    grade: Optional[str] = None
    remark: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ScoreCreate(ScoreBase):
    """Schema for creating a new score entry"""

    pass


class ScoreUpdate(BaseModel):
    """Schema for updating an existing score entry"""

    class_score: Optional[float] = Field(None, ge=0, le=30)
    exam_score: Optional[float] = Field(None, ge=0, le=70)
    term: Optional[str] = None
    academic_year: Optional[str] = None
