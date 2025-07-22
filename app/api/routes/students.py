# app/routers/students.py

# GLOBAL
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# CUSTOM
from app.core.dependencies import get_db, get_current_user
from app.crud.student import (
    create_student as cs,
    get_students as gss,
    get_student as gs,
    update_student as us,
    delete_student as ds,
)
from app.models.user import User, RoleEnum
from app.schemas.student import StudentCreate, StudentOut


router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can add students")
    return cs(db, student)


@router.get("/", response_model=List[StudentOut])
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gss(db, skip, limit)


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gs(db, student_id)


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update students")
    return us(db, student_id, student)


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete students")
    return ds(db, student_id)
