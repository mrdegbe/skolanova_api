# app/models/score.py

from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base
from app.models.enums import ScoreStatus, TermEnum


class Score(Base):
    __tablename__ = "scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    term = Column(
        Enum(
            TermEnum,
            name="termenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)

    class_score = Column(Float, nullable=False)  # max 30
    exam_score = Column(Float, nullable=False)  # max 70
    total_score = Column(Float, nullable=True)  # auto-calculated
    grade = Column(String, nullable=True)
    remark = Column(String, nullable=True)

    status = Column(
        Enum(
            ScoreStatus,
            name="scorestatusenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships (optional for joins)
    student = relationship("Student", back_populates="scores")
    subject = relationship("Subject", back_populates="scores")
    class_ = relationship("Class", back_populates="scores")
    tenant = relationship("Tenant", back_populates="scores")
    academic_year = relationship("AcademicYear", back_populates="scores")

    def __repr__(self):
        return f"<Score id={self.id} student_id={self.student_id} subject_id={self.subject_id}>"

    def __str__(self):
        return self.__repr__()
