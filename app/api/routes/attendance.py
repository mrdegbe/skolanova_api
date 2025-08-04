# app/routes/attendance.py

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.attendance import AttendanceHistoryOut

from app.crud.attendance import (
    create_attendance,
    get_attendance_history,
    # get_attendance_by_id,
    # get_attendance_for_student,
    # get_attendance_for_class_date,
    # update_attendance,
    # delete_attendance,
)
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


@router.post("/", response_model=List[AttendanceOut], status_code=201)
def create(
    attendance_in: AttendanceCreate, db: Session = Depends(get_db)
) -> List[AttendanceOut]:
    try:
        return create_attendance(db, attendance_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", response_model=List[AttendanceHistoryOut])
def attendance_history(
    student_id: int,
    class_id: int,
    db: Session = Depends(get_db),
):
    return get_attendance_history(db, student_id, class_id)


# @router.get("/{attendance_id}", response_model=AttendanceOut)
# def read(attendance_id: int, db: Session = Depends(get_db)) -> AttendanceOut:
#     attendance = get_attendance_by_id(db, attendance_id)
#     if not attendance:
#         raise HTTPException(status_code=404, detail="Attendance not found")
#     return attendance


# @router.put("/{attendance_id}", response_model=AttendanceOut)
# def update(
#     attendance_id: int, attendance_in: AttendanceUpdate, db: Session = Depends(get_db)
# ) -> AttendanceOut:
#     attendance = update_attendance(db, attendance_id, attendance_in)
#     if not attendance:
#         raise HTTPException(status_code=404, detail="Attendance not found")
#     return attendance


# @router.delete("/{attendance_id}", status_code=204)
# def delete(attendance_id: int, db: Session = Depends(get_db)) -> None:
#     success = delete_attendance(db, attendance_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Attendance not found")
