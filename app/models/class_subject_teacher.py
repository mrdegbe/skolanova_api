from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class ClassSubjectTeacher(Base):
    __tablename__ = "class_subject_teacher"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(
        Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False
    )
    subject_id = Column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    teacher_id = Column(
        Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )

    # ✅ Relationships
    class_ = relationship("Class", back_populates="subject_links")
    subject = relationship("Subject", back_populates="subject_links")
    teacher = relationship("Teacher", back_populates="subject_links")

    def __repr__(self):
        return f"<ClassSubjectTeacher id={self.id} class_id={self.class_id} subject_id={self.subject_id} teacher_id={self.teacher_id}>"
    
    def __str__(self):
        return self.__repr__()
