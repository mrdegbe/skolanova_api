# app/routers/classes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.class_ import (
    create_class as cc,
    get_class as gc,
    get_classes as gcs,
    delete_class as dc,
    update_class as uc,
)
from app.schemas.class_ import Class, ClassBase, ClassCreate, ClassOut, ClassUpdate
from app.core.dependencies import get_db, get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("/")
def create_class(
    class_: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create classes")
    return cc(db, class_)


@router.get("/", response_model=List[ClassOut])
def get_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # if current_user.role != models.RoleEnum.admin:
    #     raise HTTPException(status_code=403, detail="Only admins can get classes")

    return gcs(db, skip, limit)


@router.get("/{class_id}", response_model=ClassOut)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gc(db, class_id)


@router.put("/{class_id}")
def update_class(
    class_id: int,
    class_: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update classes")
    return uc(db, class_id, class_)


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete classes")
    return dc(db, class_id)
