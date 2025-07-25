from sqlalchemy import Column, Integer, String, Date, func, DateTime, Boolean, event
from sqlalchemy.orm import relationship
from app.core.database import Base


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "2024/2025"
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=False, nullable=False)
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
    results = relationship("Result", back_populates="academic_year")
    classes = relationship("Class", back_populates="academic_year")

    def __repr__(self):
        return f"<AcademicYear id={self.id} name={self.name}>"

    def __str__(self):
        return self.__repr__()


# ✅ Event listener to ensure only one active year
@event.listens_for(AcademicYear, "before_insert")
@event.listens_for(AcademicYear, "before_update")
def enforce_single_active_academic_year(mapper, connection, target):
    if target.is_active:
        AcademicYear_tbl = AcademicYear.__table__
        connection.execute(
            AcademicYear_tbl.update()
            .where(AcademicYear_tbl.c.id != target.id)
            .values(is_active=False)
        )
