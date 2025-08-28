# app/crud/crud_attendance.py

from typing import Optional
from sqlalchemy.orm import Session
from app.models.academic_year import AcademicYear
from app.models.user import User
from app.models.attendance import Attendance
from app.models.enums import AttendanceStatusEnum
from app.models.teacher import Teacher
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from sqlalchemy.exc import IntegrityError

from app.models.attendance import Attendance
from app.models.student import Student
from app.models.class_ import Class
from app.models.user import User

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.attendance import Attendance  # adjust import as needed
from app.schemas.attendance import (
    AttendanceCreate,
)  # or BatchAttendanceCreate if named so
from datetime import date, datetime


def create_attendance(db: Session, attendance_in: AttendanceCreate, current_user: User):
    # 1. Validate teacher (must belong to current tenant)
    teacher = (
        db.query(Teacher)
        .filter(
            Teacher.user_id == attendance_in.marked_by,
            Teacher.tenant_id == current_user.tenant_id,
        )
        .first()
    )
    if not teacher:
        raise HTTPException(
            status_code=403,
            detail="Only teachers from this tenant can mark attendance.",
        )

    # 2. Validate academic year and class (must belong to same tenant)
    academic_year = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.id == attendance_in.academic_year_id,
            AcademicYear.tenant_id == current_user.tenant_id,
        )
        .first()
    )
    if not academic_year:
        raise HTTPException(
            status_code=404, detail="Academic year not found for this tenant."
        )

    class_obj = (
        db.query(Class)
        .filter(
            Class.id == attendance_in.class_id,
            Class.tenant_id == current_user.tenant_id,
        )
        .first()
    )
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found for this tenant.")

    saved_records = []

    for record in attendance_in.records:
        # 3. Validate student (must belong to same tenant)
        student = (
            db.query(Student)
            .filter(
                Student.id == record.student_id,
                Student.tenant_id == current_user.tenant_id,
            )
            .first()
        )
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student {record.student_id} not found in this tenant.",
            )

        attendance = Attendance(
            student_id=student.id,
            class_id=class_obj.id,
            academic_year_id=academic_year.id,
            date=attendance_in.date,
            status=record.status,
            remark=getattr(record, "note", None),
            marked_by=teacher.id,
            tenant_id=current_user.tenant_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(attendance)
        try:
            db.commit()
            db.refresh(attendance)
            saved_records.append(attendance)
        except IntegrityError:
            db.rollback()
            # Skip duplicates quietly
            continue

    if not saved_records:
        raise HTTPException(
            status_code=400,
            detail="No new attendance records saved. Possible duplicates.",
        )

    return saved_records


# def create_attendance(db: Session, attendance_in: AttendanceCreate):
#     teacher = (
#         db.query(Teacher).filter(Teacher.user_id == attendance_in.marked_by).first()
#     )
#     if not teacher:
#         raise HTTPException(
#             status_code=403, detail="Only teachers can mark attendance."
#         )

#     saved_records = []

#     for record in attendance_in.records:
#         attendance = Attendance(
#             student_id=record.student_id,
#             class_id=attendance_in.class_id,
#             academic_year_id=attendance_in.academic_year_id,
#             date=attendance_in.date,
#             status=record.status,
#             remark=record.note if hasattr(record, "note") else None,
#             marked_by=teacher.id,
#             created_at=datetime.utcnow(),
#             updated_at=datetime.utcnow(),
#         )

#         db.add(attendance)
#         try:
#             db.commit()
#             db.refresh(attendance)
#             saved_records.append(attendance)
#         except IntegrityError:
#             db.rollback()
#             # Skipping duplicates instead of raising, or you can accumulate errors
#             continue

#     if not saved_records:
#         raise HTTPException(
#             status_code=400,
#             detail="No new attendance records saved. Possible duplicates.",
#         )

#     return saved_records


def get_attendance_history(
    db: Session,
    tenant_id: str,
    class_id: Optional[int] = None,
    student_id: Optional[int] = None,
):
    query = (
        db.query(
            Attendance.id,
            Attendance.date,
            (Student.first_name + " " + Student.last_name).label("student_name"),
            Class.name.label("class_name"),
            Attendance.status,
            Attendance.remark.label("note"),
            User.name.label("marked_by"),
        )
        .join(Student, Attendance.student_id == Student.id)
        .join(Class, Attendance.class_id == Class.id)
        .outerjoin(Teacher, Attendance.marked_by == Teacher.id)  # join Teacher
        .outerjoin(User, Teacher.user_id == User.id)  # then User
        .filter(
            Attendance.tenant_id == tenant_id,
            Student.tenant_id == tenant_id,
            Class.tenant_id == tenant_id,
        )
    )

    if class_id:
        query = query.filter(Attendance.class_id == class_id)

    if student_id:
        query = query.filter(Attendance.student_id == student_id)

    return query.order_by(Attendance.date.desc()).all()
