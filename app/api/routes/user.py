# app/api/routes/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserUpdate
from app.crud import user as crud_user
from app.core import dependencies

router = APIRouter()


@router.put("/users/{user_id}")
def update_user_route(
    user_id: int, user_update: UserUpdate, db: Session = Depends(dependencies.get_db)
):
    return crud_user.update_user(db, user_id, user_update)
