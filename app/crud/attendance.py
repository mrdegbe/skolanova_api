# app/crud/crud_attendance.py

from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.enums import AttendanceStatusEnum
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from sqlalchemy.exc import IntegrityError


from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.attendance import Attendance  # adjust import as needed
from app.schemas.attendance import (
    AttendanceCreate,
)  # or BatchAttendanceCreate if named so
from datetime import datetime


def create_attendance(db: Session, attendance_in: AttendanceCreate):
    print("Creating attendance records:", attendance_in)
    saved_records = []

    for record in attendance_in.records:
        attendance = Attendance(
            student_id=record.student_id,
            class_id=attendance_in.class_id,
            academic_year_id=attendance_in.academic_year_id,
            date=attendance_in.date,
            status=record.status,
            remark=record.note if hasattr(record, "note") else None,
            marked_by=attendance_in.marked_by,
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
            # Skipping duplicates instead of raising, or you can accumulate errors
            continue

    if not saved_records:
        raise HTTPException(
            status_code=400,
            detail="No new attendance records saved. Possible duplicates.",
        )
    print("Saved attendance records:", saved_records)

    return saved_records


def get_attendance_by_id(db: Session, attendance_id: int):
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()


def get_attendance_for_class_date(db: Session, class_id: int, date):
    return (
        db.query(Attendance)
        .filter(Attendance.class_id == class_id, Attendance.date == date)
        .all()
    )


def get_attendance_for_student(db: Session, student_id: int):
    return (
        db.query(Attendance)
        .filter(Attendance.student_id == student_id)
        .order_by(Attendance.date.desc())
        .all()
    )


def update_attendance(db: Session, attendance_id: int, attendance_in: AttendanceUpdate):
    attendance = get_attendance_by_id(db, attendance_id)
    if not attendance:
        return None

    for field, value in attendance_in.dict(exclude_unset=True).items():
        setattr(attendance, field, value)

    db.commit()
    db.refresh(attendance)
    return attendance


def delete_attendance(db: Session, attendance_id: int):
    attendance = get_attendance_by_id(db, attendance_id)
    if not attendance:
        return None

    db.delete(attendance)
    db.commit()
    return True
