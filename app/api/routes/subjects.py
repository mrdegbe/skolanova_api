from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User, RoleEnum
from app.schemas.subject import SubjectCreate, SubjectOut
from app.core.dependencies import get_db, get_current_user, get_current_tenant
from app.crud.subject import (
    create_subject as cs,
    get_subjects as gss,
    get_subject as gs,
    delete_subject as ds,
    update_subject as us,
)

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=SubjectOut)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can create subjects")
    return cs(db, subject, tenant_id=tenant.id)


@router.get("/", response_model=list[SubjectOut])
def get_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    return gss(db, tenant_id=tenant.id, skip=skip, limit=limit)


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    subject = gs(db, subject_id, tenant_id=tenant.id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.put("/{subject_id}", response_model=SubjectOut)
def update_subject(
    subject_id: int,
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can update subjects")
    updated = us(db, subject_id, subject, tenant_id=tenant.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete subjects")
    deleted = ds(db, subject_id, tenant_id=tenant.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subject not found")
    return deleted
