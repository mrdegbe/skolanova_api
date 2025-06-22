# app/routers/classes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("/")
def create_class(
    _class: schemas.ClassCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create classes")
    return crud.create_class(db, _class)


@router.get("/")
def get_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_classes(db, skip, limit)


@router.get("/{class_id}")
def get_class(
    class_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_class(db, class_id)


@router.put("/{class_id}")
def update_class(
    class_id: int,
    _class: schemas.ClassCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update classes")
    return crud.update_class(db, class_id, _class)


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete classes")
    return crud.delete_class(db, class_id)
