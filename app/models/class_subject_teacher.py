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
