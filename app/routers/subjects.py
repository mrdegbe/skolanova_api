# app/routers/subjects.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/")
def create_subject(
    subject: schemas.SubjectCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create subjects")
    return crud.create_subject(db, subject)


@router.get("/")
def get_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_subjects(db, skip, limit)


@router.get("/{subject_id}")
def get_subject(
    subject_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_subject(db, subject_id)


@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    subject: schemas.SubjectCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update subjects")
    return crud.update_subject(db, subject_id, subject)


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete subjects")
    return crud.delete_subject(db, subject_id)
