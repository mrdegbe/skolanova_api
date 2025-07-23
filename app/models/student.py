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


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime(timezone=True))
    gender = Column(String)
    guardian_name = Column(String)
    guardian_contact = Column(String)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT"), nullable=False) 
    fee_status = Column(String)
    address = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    # ✅ Relationships
    class_ = relationship("Class", back_populates="students")
    results = relationship("Result", back_populates="student")
