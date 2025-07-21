# app/crud/academic_year.py

from sqlalchemy.orm import Session
from app.models.academic_year import AcademicYear as AcademicYearModel
from app.schemas.academic_year import AcademicYearCreate


def create_academic_year(db: Session, ay: AcademicYearCreate):
    db_ay = AcademicYearModel(**ay.model_dump())
    db.add(db_ay)
    db.commit()
    db.refresh(db_ay)
    return db_ay


def get_academic_years(db: Session):
    return db.query(AcademicYearModel).all()
