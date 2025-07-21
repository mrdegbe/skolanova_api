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


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "2024/2025"
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True, nullable=False)
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


# I believe it's the same concept as Academic Year

# class Year(Base):
#     __tablename__ = "years"

#     id = Column(Integer, primary_key=True, index=True)
#     year = Column(Integer, unique=True)

#     # ✅ Relationships
#     results = relationship("Result", back_populates="year")
