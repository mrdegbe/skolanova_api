# Pydantic schemas ->  [For validation]

# from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ✅ Role enum to match your models.py
# class RoleEnum(str, Enum):
#     admin = "admin"
#     teacher = "teacher"


# ✅ Request body for creating a user
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str  # Plain text from client
#     role: RoleEnum


# ✅ Response body for reading a user (optional, good for docs)
# class UserRead(BaseModel):
#     id: int
#     email: EmailStr
#     role: RoleEnum

#     class Config:
#         orm_mode = True

# ==== AUTH ====


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


# ---- STUDENT ----
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[str] = None  # ISO date string
    gender: Optional[str] = None
    guardian_name: Optional[str] = None


class StudentCreate(StudentBase):
    class_id: int  # link to a Class


class StudentOut(StudentBase):
    id: int
    class_id: int

    class Config:
        orm_mode = True


# ---- CLASS ----
class ClassBase(BaseModel):
    name: str
    teacher_id: int


class ClassCreate(ClassBase):
    name: str
    # pass


class ClassOut(ClassBase):
    id: int

    class Config:
        orm_mode = True


# ---- SUBJECT ----


class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class SubjectOut(SubjectBase):
    id: int

    class Config:
        orm_mode = True


# ---- TEACHER ----


# Input
class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


# DB + internal use
class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    user_id: int


# Output
class TeacherResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True

class TeacherOut(BaseModel):
    id: int
    name: str
    subjects: List[str] = []    # or Optional[List[str]]
    classes: List[str] = []
    contact: str
    status: str

    class Config:
        orm_mode = True


# ---- YEAR ----
class YearBase(BaseModel):
    year: int


class YearCreate(YearBase):
    pass


class YearOut(YearBase):
    id: int

    class Config:
        orm_mode = True


# ---- RESULT ----


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
        orm_mode = True


class ResultUpdate(BaseModel):
    score: float


# ---- REMARK ----
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


# ---- ClassSubjectTeacherBase ----
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
