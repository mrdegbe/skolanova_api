from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, auth, models

router = APIRouter(prefix="/class-subject-teacher", tags=["ClassSubjectTeacher"])


@router.post("/")
def create_link(
    link: schemas.ClassSubjectTeacherCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(
            status_code=403, detail="Only admins can assign subjects to teachers"
        )
    return crud.create_class_subject_teacher(db, link)


@router.get("/")
def read_links(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_class_subject_teachers(db, skip, limit)


@router.delete("/{link_id}")
def delete_link(
    link_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(
            status_code=403, detail="Only admins can delete subject-teacher links"
        )
    return crud.delete_class_subject_teacher(db, link_id)
