# ✅ << user CRUD helpers, get by email, create user etc.

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only fields that were sent
    if user_update.name is not None:
        user.name = user_update.name

    db.commit()
    db.refresh(user)
    return user
