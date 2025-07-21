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


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    # ✅ Relationships
    results = relationship("Result", back_populates="subject")
    subject_links = relationship("ClassSubjectTeacher", back_populates="subject")
