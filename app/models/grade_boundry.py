from sqlalchemy import Column, String, Float

from app.core.database import Base


class GradeBoundary(Base):
    __tablename__ = "grade_boundaries"

    grade = Column(String, primary_key=True)  # e.g., "A+"
    min_score = Column(Float, nullable=False)  # e.g., 90
    max_score = Column(Float, nullable=False)  # e.g., 100
    remark = Column(String, nullable=False)  # e.g., "Excellent"

    def __repr__(self):
        return f"<GradeBoundary grade={self.grade} min_score={self.min_score} max_score={self.max_score}>"

    def __str__(self):
        return self.__repr__()
