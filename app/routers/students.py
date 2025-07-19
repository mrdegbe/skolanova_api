# app/routers/students.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can add students")
    return crud.create_student(db, student)


@router.get("/", response_model=List[schemas.StudentOut])
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_students(db, skip, limit)


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_student(db, student_id)


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update students")
    return crud.update_student(db, student_id, student)


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete students")
    return crud.delete_student(db, student_id)
