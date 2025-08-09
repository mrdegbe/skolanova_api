from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.schemas.class_subject_teacher import (
    ClassSubjectTeacherCreate,
)
from app.models.class_subject_teacher import ClassSubjectTeacher


def create_class_subject_teacher(
    db: Session, link: ClassSubjectTeacherCreate, tenant_id: int
):
    db_link = ClassSubjectTeacher(**link.model_dump(), tenant_id=tenant_id)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_class_subject_teacher(db: Session, link_id: int, tenant_id: int):
    return (
        db.query(ClassSubjectTeacher)
        .filter(
            ClassSubjectTeacher.id == link_id,
            ClassSubjectTeacher.tenant_id == tenant_id,
        )
        .first()
    )


def get_class_subject_teachers(
    db: Session, tenant_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(ClassSubjectTeacher)
        .filter(ClassSubjectTeacher.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_class_subject_teacher(db: Session, link_id: int, tenant_id: int):
    link = get_class_subject_teacher(db, link_id, tenant_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return {"ok": True}


# from fastapi import HTTPException
# from sqlalchemy.orm import Session, joinedload

# from app.schemas.class_subject_teacher import (
#     ClassSubjectTeacher,
#     ClassSubjectTeacherCreate,
#     ClassSubjectTeacherOut,
#     ClassSubjectTeacherBase,
# )


# # --- ClassSubjectTeacher ---
# def create_class_subject_teacher(db: Session, link: ClassSubjectTeacherCreate):
#     db_link = ClassSubjectTeacher(**link.model_dump())
#     db.add(db_link)
#     db.commit()
#     db.refresh(db_link)
#     return db_link


# def get_class_subject_teacher(db: Session, link_id: int):
#     return (
#         db.query(ClassSubjectTeacher).filter(ClassSubjectTeacher.id == link_id).first()
#     )


# def get_class_subject_teachers(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(ClassSubjectTeacher).offset(skip).limit(limit).all()


# def delete_class_subject_teacher(db: Session, link_id: int):
#     link = get_class_subject_teacher(db, link_id)
#     if not link:
#         raise Exception("Not found")
#     db.delete(link)
#     db.commit()
#     return {"ok": True}
