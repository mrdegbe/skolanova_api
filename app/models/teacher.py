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


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    status = Column(String, nullable=False)
    address = Column(String)
    specialization = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    homeroom_class_id = Column(Integer, ForeignKey("classes.id"))

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
