# app/schemas/score.py

from pydantic import BaseModel, Field
from typing import Optional


class ScoreBase(BaseModel):
    student_id: int = Field(..., description="ID of the student")
    subject_id: int = Field(..., description="ID of the subject")
    class_score: float = Field(..., ge=0, le=30, description="Class score (0–30)")
    exam_score: float = Field(..., ge=0, le=70, description="Exam score (0–70)")
    term: str = Field(..., description="Term (e.g. 'Term 1', 'Term 2', 'Term 3')")
    academic_year_id: int = Field(..., description="ID of the Academic year")


class ScoreCreate(ScoreBase):
    """Schema for creating a new score entry"""
    pass


class ScoreUpdate(BaseModel):
    """Schema for updating an existing score entry"""
    class_score: Optional[float] = Field(None, ge=0, le=30)
    exam_score: Optional[float] = Field(None, ge=0, le=70)
    term: Optional[str] = None
    academic_year: Optional[str] = None
