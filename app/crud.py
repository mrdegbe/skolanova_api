# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas


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


# --- CLASSES ---
def create_class(db: Session, _class: schemas.ClassCreate):
    db_class = models.Class(**_class.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Class).offset(skip).limit(limit).all()


def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()


def update_class(db: Session, class_id: int, _class: schemas.ClassCreate):
    db_class = get_class(db, class_id)
    if not db_class:
        raise Exception("Class not found")
    for key, value in _class.dict().items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class


def delete_class(db: Session, class_id: int):
    db_class = get_class(db, class_id)
    if not db_class:
        raise Exception("Class not found")
    db.delete(db_class)
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
    for key, value in result.dict().items():
        setattr(db_result, key, value)
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


# --- TEACHERS ---
def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()


def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()


def update_teacher(db: Session, teacher_id: int, teacher: schemas.TeacherCreate):
    db_teacher = get_teacher(db, teacher_id)
    if not db_teacher:
        raise Exception("Teacher not found")
    for key, value in teacher.dict().items():
        setattr(db_teacher, key, value)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if not db_teacher:
        raise Exception("Teacher not found")
    db.delete(db_teacher)
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
