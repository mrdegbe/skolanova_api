# app/routers/subjects.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User, RoleEnum
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectOut
from app.core.dependencies import get_db, get_current_user
from app.crud.subject import (
    create_subject as cs,
    get_subjects as gss,
    get_subject as gs,
    delete_subject as ds,
    update_subject as us,
)

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/")
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create subjects")
    return cs(db, subject)


@router.get("/")
def get_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gss(db, skip, limit)


@router.get("/{subject_id}")
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gs(db, subject_id)


@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update subjects")
    return us(db, subject_id, subject)


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete subjects")
    return ds(db, subject_id)
