# app/routers/classes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth
from app.cruds import classes

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("/")
def create_class(
    _class: schemas.ClassCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create classes")
    return classes.create_class(db, _class)


@router.get("/", response_model=List[schemas.ClassOut])
def get_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # if current_user.role != models.RoleEnum.admin:
    #     raise HTTPException(status_code=403, detail="Only admins can get classes")

    return classes.get_classes(db, skip, limit)


@router.get("/{class_id}")
def get_class(
    class_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return classes.get_class(db, class_id)


@router.put("/{class_id}")
def update_class(
    class_id: int,
    _class: schemas.ClassCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update classes")
    return classes.update_class(db, class_id, _class)


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete classes")
    return classes.delete_class(db, class_id)
