from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Custom
from app.core.dependencies import get_db, get_current_user
from app.models.user import User, RoleEnum
from app.schemas.teacher import (
    TeacherCreate,
    TeacherUpdate,
    TeacherBase,
    TeacherResponse,
    TeacherOut,
)
from app.crud.teacher import (
    create_teacher as ct,
    get_teachers as gts,
    get_teacher as gt,
    update_teacher as ut,
    delete_teacher as dt,
)

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("/")
def create_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create teachers")

    return ct(db, teacher_data)


@router.get("/", response_model=List[TeacherOut])
def get_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gts(db, skip, limit)


@router.get("/{teacher_id}")
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gt(db, teacher_id)


@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: int,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update teachers")
    return ut(db, teacher_id, teacher_data)


@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete teachers")
    return dt(db, teacher_id)
