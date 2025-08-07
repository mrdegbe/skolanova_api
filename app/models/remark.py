from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class Remark(Base):
    __tablename__ = "remarks"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=True,  # Set to False after backfilling
        index=True,
    )
    result_id = Column(Integer, ForeignKey("results.id", ondelete="CASCADE"))
    teacher_id = Column(
        Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    comment = Column(String)

    # ✅ Relationships
    result = relationship("Result", back_populates="remarks")
    teacher = relationship("Teacher")
    tenant = relationship("Tenant", back_populates="remarks")

    def __repr__(self):
        return f"<Remark id={self.id} result_id={self.result_id}>"

    def __str__(self):
        return self.__repr__()
