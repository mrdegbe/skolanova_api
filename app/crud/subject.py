from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate


def create_subject(db: Session, subject: SubjectCreate, tenant_id: int):
    db_subject = Subject(**subject.model_dump(), tenant_id=tenant_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_subjects(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Subject)
        .filter(Subject.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_subject(db: Session, subject_id: int, tenant_id: int):
    return (
        db.query(Subject)
        .filter(Subject.id == subject_id, Subject.tenant_id == tenant_id)
        .first()
    )


def update_subject(
    db: Session, subject_id: int, subject: SubjectCreate, tenant_id: int
):
    db_subject = get_subject(db, subject_id, tenant_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in subject.model_dump().items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def delete_subject(db: Session, subject_id: int, tenant_id: int):
    db_subject = get_subject(db, subject_id, tenant_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(db_subject)
    db.commit()
    return {"ok": True}


# from fastapi import HTTPException
# from sqlalchemy.orm import Session, joinedload
# from app.models.subject import Subject
# from app.schemas.subject import SubjectBase, SubjectCreate, SubjectOut


# def create_subject(db: Session, subject: SubjectCreate):
#     db_subject = Subject(**subject.model_dump())
#     db.add(db_subject)
#     db.commit()
#     db.refresh(db_subject)
#     return db_subject


# def get_subjects(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Subject).offset(skip).limit(limit).all()


# def get_subject(db: Session, subject_id: int):
#     return db.query(Subject).filter(Subject.id == subject_id).first()


# def update_subject(db: Session, subject_id: int, subject: SubjectCreate):
#     db_subject = get_subject(db, subject_id)
#     if not db_subject:
#         raise Exception("Subject not found")
#     for key, value in subject.model_dump().items():
#         setattr(db_subject, key, value)
#     db.commit()
#     db.refresh(db_subject)
#     return db_subject


# def delete_subject(db: Session, subject_id: int):
#     db_subject = get_subject(db, subject_id)
#     if not db_subject:
#         raise Exception("Subject not found")
#     db.delete(db_subject)
#     db.commit()
#     return {"ok": True}
