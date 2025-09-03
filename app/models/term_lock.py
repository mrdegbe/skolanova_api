from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Boolean,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID

from app.models.enums import TermEnum


class TermLock(Base):
    __tablename__ = "term_locks"

    id = Column(Integer, primary_key=True, index=True)

    academic_year_id = Column(
        Integer,
        ForeignKey("academic_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    term = Column(
        Enum(
            TermEnum,
            name="termenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )  # e.g. "Term 1", "Term 2", "Term 3"

    is_locked = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tenant_id = Column(
        UUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # ✅ Relationships
    academic_year = relationship("AcademicYear", back_populates="term_locks")
    class_ = relationship("Class", back_populates="term_locks")
    tenant = relationship("Tenant", back_populates="term_locks")

    __table_args__ = (
        UniqueConstraint(
            "academic_year_id", "class_id", "term", "tenant_id", name="uq_term_lock"
        ),
    )

    def __repr__(self):
        return f"<TermLock year={self.academic_year_id} class={self.class_id} term={self.term} locked={self.is_locked}>"
