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
    class_id: int
    subject_id: int
    teacher_id: int

    class Config:
        orm_mode = True
