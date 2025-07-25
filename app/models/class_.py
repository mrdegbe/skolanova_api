from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    func,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    academic_year_id = Column(
        Integer, ForeignKey("academic_years.id"), nullable=False
    )  # New!
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

    __table_args__ = (
        UniqueConstraint("name", "academic_year_id", name="uq_class_name_year"),
    )

    # ✅ Relationships
    academic_year = relationship("AcademicYear", back_populates="classes")
    students = relationship("Student", back_populates="class_")
    subject_links = relationship("ClassSubjectTeacher", back_populates="class_")
    class_teacher = relationship(
        "Teacher", foreign_keys=[class_teacher_id], back_populates="homeroom_classes"
    )

    def __repr__(self):
        return f"<Class id={self.id} name={self.name}>"
    
    def __str__(self):
        return self.__repr__()
