from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.class_ import Class
from app.models.student import Student
from app.schemas.student import StudentBase, StudentCreate, StudentOut


def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    students = (
        db.query(Student)
        .options(joinedload(Student.class_).joinedload(Class.academic_year))
        .all()
    )
    result = []
    for student in students:
        result.append(
            {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "date_of_birth": student.date_of_birth,
                "gender": student.gender,
                "guardian_name": student.guardian_name,
                "guardian_contact": student.guardian_contact,
                "class_id": student.class_id,
                "fee_status": student.fee_status,
                "address": student.address,
                "class_name": student.class_.name if student.class_ else None,
                "academic_year_id": (
                    student.class_.academic_year.id
                    if student.class_ and student.class_.academic_year
                    else None
                ),
                "academic_year_name": (
                    student.class_.academic_year.name
                    if student.class_ and student.class_.academic_year
                    else None
                ),
                "created_at": student.created_at,
                "updated_at": student.updated_at,
            }
        )
    return result


def get_student(db: Session, student_id: int):
    student = (
        db.query(Student)
        .options(joinedload(Student.class_).joinedload(Class.academic_year))
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        return None

    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "date_of_birth": student.date_of_birth,
        "gender": student.gender,
        "guardian_name": student.guardian_name,
        "guardian_contact": student.guardian_contact,
        "class_id": student.class_id,
        "fee_status": student.fee_status,
        "address": student.address,
        "class_name": student.class_.name if student.class_ else None,
        "academic_year_id": (
            student.class_.academic_year.id
            if student.class_ and student.class_.academic_year
            else None
        ),
        "academic_year_name": (
            student.class_.academic_year.name
            if student.class_ and student.class_.academic_year
            else None
        ),
        "created_at": student.created_at,
        "updated_at": student.updated_at,
    }


def update_student(db: Session, student_id: int, student: StudentCreate):
    db_student = get_student(db, student_id)
    if not db_student:
        raise Exception("Student not found")
    for key, value in student.model_dump().items():
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
