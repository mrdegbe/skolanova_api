from sqlalchemy import Column, Integer, ForeignKey, Float, Enum, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from sqlalchemy.dialects.postgresql import UUID

from app.models.enums import TermEnum


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=True,  # Set to False after backfilling
        index=True,
    )
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    academic_year_id = Column(
        Integer, ForeignKey("academic_years.id", ondelete="CASCADE"), index=True
    )
    score = Column(Float)
    term = Column(Enum(TermEnum), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "term",
            "academic_year_id",
            name="uq_result_unique",
        ),
    )

    # ✅ Relationships
    remarks = relationship("Remark", back_populates="result")
    student = relationship("Student", back_populates="results")
    subject = relationship("Subject", back_populates="results")
    academic_year = relationship("AcademicYear", back_populates="results")
    tenant = relationship("Tenant", back_populates="results")

    def __repr__(self):
        return f"<Result id={self.id} student_id={self.student_id} subject_id={self.subject_id}>"

    def __str__(self):
        return self.__repr__()
