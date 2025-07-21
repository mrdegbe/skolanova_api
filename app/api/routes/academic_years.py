# app/routers/academic_years.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Custom Imports
from app.schemas.academic_year import AcademicYear, AcademicYearCreate
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/academic_years", tags=["AcademicYears"])


@router.post("/", response_model=AcademicYear)
def create_academic_year(ay: AcademicYearCreate, db: Session = Depends(get_db)):
    db_ay = AcademicYear(**ay.model_dump())
    db.add(db_ay)
    db.commit()
    db.refresh(db_ay)
    return db_ay


@router.get("/", response_model=List[AcademicYear])
def list_academic_years(db: Session = Depends(get_db)):
    return db.query(AcademicYear).all()
