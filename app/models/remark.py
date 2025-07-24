from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Remark(Base):
    __tablename__ = "remarks"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    comment = Column(String)

    # ✅ Relationships
    result = relationship("Result", back_populates="remarks")
    teacher = relationship("Teacher")
