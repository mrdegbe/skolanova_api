import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)  # used for subdomain
    school_logo = Column(String, nullable=True)  # URL or path to logo

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    academic_years = relationship("AcademicYear", back_populates="tenant")
    attendance = relationship("Attendance", back_populates="tenant")
    classes = relationship("Class", back_populates="tenant")
    class_subject_teachers = relationship(
        "ClassSubjectTeacher", back_populates="tenant"
    )
    remarks = relationship("Remark", back_populates="tenant")
    results = relationship("Result", back_populates="tenant")
    students = relationship("Student", back_populates="tenant")
    subjects = relationship("Subject", back_populates="tenant")
    teachers = relationship("Teacher", back_populates="tenant")
    users = relationship("User", back_populates="tenant")
