from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import GenderEnum, TeacherStatusEnum


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(
        Enum(
            GenderEnum,
            name="genderenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    contact = Column(String, nullable=False)
    status = Column(
        Enum(
            TeacherStatusEnum,
            name="teacherstatusenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    address = Column(String)
    specialization = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    @property
    def email(self):
        return self.user.email if self.user else None

    # ✅ Relationships
    homeroom_classes = relationship(
        "Class",
        foreign_keys="[Class.class_teacher_id]",
        back_populates="class_teacher",
    )
    user = relationship("User", back_populates="teacher")
    subject_links = relationship("ClassSubjectTeacher", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher id={self.id} name={self.first_name} {self.last_name}>"

    def __str__(self):
        return self.__repr__()
