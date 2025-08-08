from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    func,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import ClassStatusEnum
from sqlalchemy.dialects.postgresql import UUID


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(
        Enum(
            ClassStatusEnum,
            name="classstatusenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    # Foreign keys
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,  # Set to False after backfilling
        index=True,
    )
    academic_year_id = Column(
        Integer, ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False
    )
    class_teacher_id = Column(
        Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint("name", "academic_year_id", name="uq_class_name_year"),
    )

    # ✅ Relationships
    tenant = relationship("Tenant", back_populates="classes")
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
