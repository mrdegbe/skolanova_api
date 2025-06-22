# app/routers/results.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("/")
def create_result(
    result: schemas.ResultCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in [models.RoleEnum.admin, models.RoleEnum.teacher]:
        raise HTTPException(
            status_code=403, detail="Only teachers or admins can create results"
        )
    return crud.create_result(db, result)


@router.get("/")
def get_results(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_results(db, skip, limit)


@router.get("/{result_id}")
def get_result(
    result_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_result(db, result_id)


@router.put("/{result_id}")
def update_result(
    result_id: int,
    result: schemas.ResultCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in [models.RoleEnum.admin, models.RoleEnum.teacher]:
        raise HTTPException(
            status_code=403, detail="Only teachers or admins can update results"
        )
    return crud.update_result(db, result_id, result)


@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete results")
    return crud.delete_result(db, result_id)
