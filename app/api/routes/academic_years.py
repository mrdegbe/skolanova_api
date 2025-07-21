# app/api/routes/academic_years.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.academic_year import (
    AcademicYear as AcademicYearSchema,
    AcademicYearCreate,
)
from app.core.dependencies import get_db
from app.crud.academic_year import (
    create_academic_year as crud_create_ay,
    get_academic_years,
)

router = APIRouter(prefix="/academic_years", tags=["AcademicYears"])


@router.post("/", response_model=AcademicYearSchema)
def create_academic_year(ay: AcademicYearCreate, db: Session = Depends(get_db)):
    return crud_create_ay(db, ay)


@router.get("/", response_model=List[AcademicYearSchema])
def list_academic_years(db: Session = Depends(get_db)):
    return get_academic_years(db)
