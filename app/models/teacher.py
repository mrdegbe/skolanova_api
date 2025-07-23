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


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    contact = Column(String)
    status = Column(String)
    address = Column(String)
    specialization = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    homeroom_class_id = Column(Integer, ForeignKey("classes.id"))

    @property
    def email(self):
        return self.user.email if self.user else None

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    # ✅ Relationships
    user = relationship("User", back_populates="teacher")
    subject_links = relationship("ClassSubjectTeacher", back_populates="teacher")
    homeroom_class = relationship(
        "Class",
        foreign_keys="Class.class_teacher_id",
        back_populates="class_teacher",
        uselist=False   # 👉 Make it one-to-one
    )
