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
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), index=True)
    score = Column(Float)
    term = Column(Enum(TermEnum), nullable=False)

    # ✅ Relationships
    remarks = relationship("Remark", back_populates="result")
    student = relationship("Student", back_populates="results")
    subject = relationship("Subject", back_populates="results")
    academic_year = relationship("AcademicYear", back_populates="results")

    def __repr__(self):
        return f"<Result id={self.id} student_id={self.student_id} subject_id={self.subject_id}>"

    def __str__(self):
        return self.__repr__()
