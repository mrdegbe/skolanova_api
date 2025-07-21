from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Date,
    Enum,
    func,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TermEnum(str, enum.Enum):
    term1 = "Term 1"
    term2 = "Term 2"
    term3 = "Term 3"


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"))
    score = Column(Float)
    term = Column(Enum(TermEnum), nullable=False)

    # ✅ Relationships
    student = relationship("Student", back_populates="results")
    subject = relationship("Subject", back_populates="results")
    academic_year = relationship("AcademicYear", back_populates="results")
    remarks = relationship("Remark", back_populates="result")
