from typing import Optional
from pydantic import BaseModel, EmailStr


class ClassSubjectTeacherBase(BaseModel):
    class_id: int
    subject_id: int
    teacher_id: int

class ClassSubjectTeacherCreate(ClassSubjectTeacherBase):
    pass

class ClassSubjectTeacher(ClassSubjectTeacherBase):
    id: int

    class Config:
        orm_mode = True

class ClassSubjectTeacherOut(BaseModel):
    id: int
    class_id: Optional[int] = None  # ✅ FIXED
    subject_id: int
    teacher_id: int
    class_name: Optional[str] = None
    subject_name: Optional[str] = None

    class Config:
        orm_mode = True
