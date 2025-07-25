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
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"))
    comment = Column(String)

    # ✅ Relationships
    result = relationship("Result", back_populates="remarks")
    teacher = relationship("Teacher")

    def __repr__(self):
        return f"<Remark id={self.id} result_id={self.result_id}>"

    def __str__(self):
        return self.__repr__()
