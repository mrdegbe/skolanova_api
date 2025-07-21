from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User, RoleEnum
from app.core.dependencies import get_db, get_current_user
from app.schemas.class_subject_teacher import (
    ClassSubjectTeacherCreate,
    ClassSubjectTeacherBase,
    ClassSubjectTeacher,
    ClassSubjectTeacherOut,
)
from app.crud.class_subject_teacher import (
    create_class_subject_teacher as ccst,
    get_class_subject_teachers as gcsts,
    get_class_subject_teacher as gcst,
    delete_class_subject_teacher as dcst,
)

router = APIRouter(prefix="/class-subject-teacher", tags=["ClassSubjectTeacher"])


@router.post("/")
def create_link(
    link: ClassSubjectTeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403, detail="Only admins can assign subjects to teachers"
        )
    return ccst(db, link)


@router.get("/")
def read_links(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can do this!")
    return gcsts(db, skip, limit)


@router.delete("/{link_id}")
def delete_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403, detail="Only admins can delete subject-teacher links"
        )
    return dcst(db, link_id)
