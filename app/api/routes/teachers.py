from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, get_current_tenant
from app.models.user import User, RoleEnum
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherOut
from app.crud import teacher as teacher_crud

router = APIRouter(prefix="/teachers", tags=["Teachers"])


def require_admin(user: User) -> None:
    """Raise 403 if the current user is not an admin."""
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can perform this action")


@router.post("/", response_model=TeacherOut)
def create_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    require_admin(current_user)
    return teacher_crud.create_teacher(db, teacher_data, tenant_id=tenant.id)


@router.get("/", response_model=List[TeacherOut])
def list_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    return teacher_crud.get_teachers(db, tenant_id=tenant.id, skip=skip, limit=limit)


@router.get("/{teacher_id}", response_model=TeacherOut)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    return teacher_crud.get_teacher(db, teacher_id, tenant_id=tenant.id)


@router.put("/{teacher_id}", response_model=TeacherOut)
def update_teacher(
    teacher_id: int,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    require_admin(current_user)
    return teacher_crud.update_teacher(db, teacher_id, teacher_data, tenant_id=tenant.id)


@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    require_admin(current_user)
    return teacher_crud.delete_teacher(db, teacher_id, tenant_id=tenant.id)
