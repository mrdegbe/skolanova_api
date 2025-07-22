# app/crud/academic_year.py

from sqlalchemy.orm import Session
from app.models.academic_year import AcademicYear as AcademicYearModel
from app.schemas.academic_year import AcademicYearCreate


def create_academic_year(db: Session, ay: AcademicYearCreate):

    if ay.is_active:
        db.query(AcademicYearModel).update({AcademicYearModel.is_active: False})

    db_ay = AcademicYearModel(**ay.model_dump())
    db.add(db_ay)
    db.commit()
    db.refresh(db_ay)
    return db_ay


def get_academic_years(db: Session):
    return db.query(AcademicYearModel).all()


def get_academic_year(db: Session, ay_id: int):
    return db.query(AcademicYearModel).filter(AcademicYearModel.id == ay_id).first()


def update_academic_year(db: Session, ay_id: int, ay_update: AcademicYearCreate):
    db_ay = db.query(AcademicYearModel).filter(AcademicYearModel.id == ay_id).first()
    if db_ay is None:
        return None

    # If setting this academic year to active, deactivate all others first
    if ay_update.is_active:
        db.query(AcademicYearModel).update({AcademicYearModel.is_active: False})

    for key, value in ay_update.model_dump().items():
        setattr(db_ay, key, value)
    db.commit()
    db.refresh(db_ay)
    return db_ay


def delete_academic_year(db: Session, ay_id: int):
    db_ay = db.query(AcademicYearModel).filter(AcademicYearModel.id == ay_id).first()
    if db_ay is None:
        return None
    db.delete(db_ay)
    db.commit()
    return db_ay
