# app/routers/students.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, get_current_tenant
from app.crud.student import (
    create_student as create_student_crud,
    get_students as get_students_crud,
    get_student as get_student_crud,
    update_student as update_student_crud,
    delete_student as delete_student_crud,
)
from app.models.user import User, RoleEnum
from app.models.tenant import Tenant
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut

router = APIRouter(prefix="/students", tags=["Students"])


# -----------------------------
# Create
# -----------------------------
@router.post("/", response_model=StudentOut)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can add students")
    return create_student_crud(db, student, tenant.id)


# -----------------------------
# List
# -----------------------------
@router.get("/", response_model=List[StudentOut])
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
):
    return get_students_crud(db, tenant.id, skip, limit)


# -----------------------------
# Retrieve
# -----------------------------
@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
):
    student = get_student_crud(db, student_id, tenant.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# -----------------------------
# Update
# -----------------------------
@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update students")
    return update_student_crud(db, student_id, student, tenant.id)


# -----------------------------
# Delete
# -----------------------------
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete students")
    return delete_student_crud(db, student_id, tenant.id)
