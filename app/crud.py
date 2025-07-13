# app/crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from . import models, auth, schemas
import secrets, string


# --- STUDENTS ---
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if not db_student:
        raise Exception("Student not found")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if not db_student:
        raise Exception("Student not found")
    db.delete(db_student)
    db.commit()
    return {"ok": True}





# --- SUBJECTS ---
def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()


def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()


def update_subject(db: Session, subject_id: int, subject: schemas.SubjectCreate):
    db_subject = get_subject(db, subject_id)
    if not db_subject:
        raise Exception("Subject not found")
    for key, value in subject.dict().items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if not db_subject:
        raise Exception("Subject not found")
    db.delete(db_subject)
    db.commit()
    return {"ok": True}


# --- RESULTS ---
def create_result(db: Session, result: schemas.ResultCreate):
    db_result = models.Result(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Result).offset(skip).limit(limit).all()


def get_result(db: Session, result_id: int):
    return db.query(models.Result).filter(models.Result.id == result_id).first()


def update_result(db: Session, result_id: int, result: schemas.ResultCreate):
    db_result = get_result(db, result_id)
    if not db_result:
        raise Exception("Result not found")

    # ✅ Only allow changing the score — nothing else!
    db_result.score = result.score

    db.commit()
    db.refresh(db_result)
    return db_result


def delete_result(db: Session, result_id: int):
    db_result = get_result(db, result_id)
    if not db_result:
        raise Exception("Result not found")
    db.delete(db_result)
    db.commit()
    return {"ok": True}


# --- YEARS ---
def create_year(db: Session, year: schemas.YearCreate):
    db_year = models.Year(**year.dict())
    db.add(db_year)
    db.commit()
    db.refresh(db_year)
    return db_year


def get_years(db: Session):
    return db.query(models.Year).all()


# --- ClassSubjectTeacher ---
def create_class_subject_teacher(db: Session, link: schemas.ClassSubjectTeacherCreate):
    db_link = models.ClassSubjectTeacher(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_class_subject_teacher(db: Session, link_id: int):
    return (
        db.query(models.ClassSubjectTeacher)
        .filter(models.ClassSubjectTeacher.id == link_id)
        .first()
    )


def get_class_subject_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ClassSubjectTeacher).offset(skip).limit(limit).all()


def delete_class_subject_teacher(db: Session, link_id: int):
    link = get_class_subject_teacher(db, link_id)
    if not link:
        raise Exception("Not found")
    db.delete(link)
    db.commit()
    return {"ok": True}


# --- Users ---
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update.name
    db.commit()
    db.refresh(user)
    return user
