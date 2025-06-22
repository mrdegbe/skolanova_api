# app/routers/teachers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("/")
def create_teacher(
    teacher: schemas.TeacherCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create teachers")
    return crud.create_teacher(db, teacher)


@router.get("/")
def get_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_teachers(db, skip, limit)


@router.get("/{teacher_id}")
def get_teacher(
    teacher_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_teacher(db, teacher_id)


@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: int,
    teacher: schemas.TeacherCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update teachers")
    return crud.update_teacher(db, teacher_id, teacher)


@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete teachers")
    return crud.delete_teacher(db, teacher_id)
