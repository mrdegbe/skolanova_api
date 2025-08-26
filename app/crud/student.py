# app/crud/student.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.class_ import Class
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


# -----------------------------
# Create
# -----------------------------
def create_student(db: Session, student_data: StudentCreate, tenant_id: int) -> Student:
    """Create a new student belonging to a specific tenant."""
    db_student = Student(**student_data.model_dump(), tenant_id=tenant_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# -----------------------------
# Read (List)
# -----------------------------
def get_students(
    db: Session, tenant_id: int, skip: int = 0, limit: int = 100
) -> List[dict]:
    """Retrieve all students for a tenant."""
    students = (
        db.query(Student)
        .filter(Student.tenant_id == tenant_id)
        .options(joinedload(Student.class_).joinedload(Class.academic_year))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [_serialize_student(student) for student in students]


# -----------------------------
# Read (Single)
# -----------------------------
def get_student(db: Session, student_id: int, tenant_id: int) -> Optional[dict]:
    """Retrieve a single student by ID, scoped to a tenant."""
    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.tenant_id == tenant_id)
        .options(joinedload(Student.class_).joinedload(Class.academic_year))
        .first()
    )

    if not student:
        return None

    return _serialize_student(student)


# -----------------------------
# Read (By Class)
# -----------------------------
def get_students_by_class_crud(
    db: Session, class_id: int, tenant_id: str
) -> List[dict]:
    """Retrieve all students for a specific class (scoped to tenant)."""
    students = (
        db.query(Student)
        .filter(Student.class_id == class_id, Student.tenant_id == tenant_id)
        .options(joinedload(Student.class_).joinedload(Class.academic_year))
        .all()
    )

    return [_serialize_student(student) for student in students]


# -----------------------------
# Update
# -----------------------------
def update_student(
    db: Session, student_id: int, student_data: StudentUpdate, tenant_id: int
) -> Student:
    """Update an existing student."""
    db_student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.tenant_id == tenant_id)
        .first()
    )
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student_data.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


# -----------------------------
# Delete
# -----------------------------
def delete_student(db: Session, student_id: int, tenant_id: int) -> dict:
    """Delete a student by ID."""
    db_student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.tenant_id == tenant_id)
        .first()
    )
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"ok": True}


# -----------------------------
# Private Serializer
# -----------------------------
def _serialize_student(student: Student) -> dict:
    """Convert a Student ORM object into a serializable dict."""
    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "date_of_birth": student.date_of_birth,
        "gender": student.gender,
        "guardian_name": student.guardian_name,
        "guardian_contact": student.guardian_contact,
        "class_id": student.class_id,
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
        "fee_status": student.fee_status,
        "address": student.address,
        "created_at": student.created_at,
        "updated_at": student.updated_at,
    }
