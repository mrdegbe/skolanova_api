from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    func,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"))  # New!

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    class_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    class_teacher = relationship(
        "Teacher", back_populates="dedicated_class", uselist=False
    )

    academic_year = relationship("AcademicYear")
    students = relationship("Student", back_populates="class_")
    subject_links = relationship("ClassSubjectTeacher", back_populates="class_")
