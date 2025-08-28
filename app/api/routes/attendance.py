# app/routes/attendance.py

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.tenant import Tenant
from app.models.user import User
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
from app.core.dependencies import get_current_tenant, get_current_user, get_db

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


@router.post("/", response_model=List[AttendanceOut], status_code=201)
def create(
    attendance_in: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # get user from auth
) -> List[AttendanceOut]:
    try:
        return create_attendance(db, attendance_in, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.post("/", response_model=List[AttendanceOut], status_code=201)
# def create(
#     attendance_in: AttendanceCreate, db: Session = Depends(get_db)
# ) -> List[AttendanceOut]:
#     try:
#         return create_attendance(db, attendance_in)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", response_model=List[AttendanceHistoryOut])
def attendance_history(
    class_id: Optional[int] = None,
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),  # 👈 ensures tenant awareness
):
    return get_attendance_history(
        db, tenant.id, class_id=class_id, student_id=student_id
    )
