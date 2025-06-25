# app/models.py
# SQLAlchemy models

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"


class TermEnum(str, enum.Enum):
    term1 = "Term 1"
    term2 = "Term 2"
    term3 = "Term 3"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum))
    name = Column(String)  # ✅ NEW

    # ✅ Relationships
    teacher = relationship("Teacher", back_populates="user", uselist=False)


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    # ✅ Relationships
    user = relationship("User", back_populates="teacher")
    classes = relationship("Class", back_populates="teacher")
    subject_links = relationship("ClassSubjectTeacher", back_populates="teacher")


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    teacher = relationship("Teacher", back_populates="classes")
    students = relationship(
        "Student", back_populates="class_"
    )  # 'class' is a reserved keyword
    subject_links = relationship("ClassSubjectTeacher", back_populates="class_")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    guardian_name = Column(String)
    class_id = Column(Integer, ForeignKey("classes.id"))

    # ✅ Relationships
    class_ = relationship("Class", back_populates="students")
    results = relationship("Result", back_populates="student")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    # ✅ Relationships
    results = relationship("Result", back_populates="subject")
    subject_links = relationship("ClassSubjectTeacher", back_populates="subject")


class Year(Base):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True)

    # ✅ Relationships
    results = relationship("Result", back_populates="year")


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    year_id = Column(Integer, ForeignKey("years.id"))
    score = Column(Float)
    term = Column(Enum(TermEnum), nullable=False)

    # ✅ Relationships
    student = relationship("Student", back_populates="results")
    subject = relationship("Subject", back_populates="results")
    year = relationship("Year", back_populates="results")
    remarks = relationship("Remark", back_populates="result")


class Remark(Base):
    __tablename__ = "remarks"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    comment = Column(String)

    # ✅ Relationships
    result = relationship("Result", back_populates="remarks")
    teacher = relationship("Teacher")


class ClassSubjectTeacher(Base):
    __tablename__ = "class_subject_teacher"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"))

    # ✅ Relationships
    class_ = relationship("Class", back_populates="subject_links")
    subject = relationship("Subject", back_populates="subject_links")
    teacher = relationship("Teacher", back_populates="subject_links")
