from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


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

    def __repr__(self):
        return f"<Subject id={self.id} name={self.name}>"

    def __str__(self):
        return self.__repr__()
