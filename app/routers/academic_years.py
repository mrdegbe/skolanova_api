# app/routers/academic_years.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth
from app.cruds import classes

router = APIRouter(prefix="/academic_years", tags=["AcademicYears"])


@router.post("/", response_model=schemas.AcademicYear)
def create_academic_year(
    ay: schemas.AcademicYearCreate, db: Session = Depends(auth.get_db)
):
    db_ay = models.AcademicYear(**ay.model_dump())
    db.add(db_ay)
    db.commit()
    db.refresh(db_ay)
    return db_ay


@router.get("/", response_model=List[schemas.AcademicYear])
def list_academic_years(db: Session = Depends(auth.get_db)):
    return db.query(models.AcademicYear).all()
