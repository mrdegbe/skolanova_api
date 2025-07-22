# app/api/routes/academic_years.py

from fastapi import APIRouter, Depends, HTTPException
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
    get_academic_year as crud_get_ay,
    update_academic_year as crud_update_ay,
    delete_academic_year as crud_delete_ay,
)

router = APIRouter(prefix="/academic_years", tags=["AcademicYears"])


@router.post("/", response_model=AcademicYearSchema)
def create_academic_year(ay: AcademicYearCreate, db: Session = Depends(get_db)):
    return crud_create_ay(db, ay)


@router.get("/", response_model=List[AcademicYearSchema])
def list_academic_years(db: Session = Depends(get_db)):
    return get_academic_years(db)


@router.get("/{ay_id}", response_model=AcademicYearSchema)
def get_academic_year(ay_id: int, db: Session = Depends(get_db)):
    ay = crud_get_ay(db, ay_id)
    if ay is None:
        raise HTTPException(status_code=404, detail="Academic Year not found")
    return ay


@router.put("/{ay_id}", response_model=AcademicYearSchema)
def update_academic_year(
    ay_id: int, ay: AcademicYearCreate, db: Session = Depends(get_db)
):
    updated = crud_update_ay(db, ay_id, ay)
    if updated is None:
        raise HTTPException(status_code=404, detail="Academic Year not found")
    return updated


@router.delete("/{ay_id}", response_model=AcademicYearSchema)
def delete_academic_year(ay_id: int, db: Session = Depends(get_db)):
    deleted = crud_delete_ay(db, ay_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Academic Year not found")
    return deleted
