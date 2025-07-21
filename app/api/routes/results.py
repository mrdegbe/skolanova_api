# app/routers/results.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.result import ResultCreate, ResultBase, ResultOut, ResultUpdate
from app.core.dependencies import get_db, get_current_user
from app.models.user import User, RoleEnum
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.class_subject_teacher import ClassSubjectTeacher
from app.crud.result import (
    create_result as cr,
    get_results as grs,
    get_result as gr,
    update_result as ur,
    delete_result as dr
)
from app.models.result import Result

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("/")
def create_result(
    result: ResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [RoleEnum.admin, RoleEnum.teacher]:
        raise HTTPException(
            status_code=403, detail="Only teachers or admins can create results"
        )

    # ✅ If teacher: enforce subject permission
    if current_user.role == RoleEnum.teacher:
        # 1️⃣ Get Teacher profile linked to user
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=403, detail="Teacher profile not found")

        # 2️⃣ Get the student to find their class
        student = db.query(Student).filter(Student.id == result.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # 3️⃣ Check ClassSubjectTeacher link
        link = (
            db.query(ClassSubjectTeacher)
            .filter(
                ClassSubjectTeacher.class_id == student.class_id,
                ClassSubjectTeacher.subject_id == result.subject_id,
                ClassSubjectTeacher.teacher_id == teacher.id,
            )
            .first()
        )

        if not link:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to teach this subject in this class",
            )

    # ✅ If admin or verified teacher, call CRUD to create
    return cr(db, result)


@router.get("/")
def get_results(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return grs(db, skip, limit)


@router.get("/{result_id}")
def get_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return gr(db, result_id)


@router.put("/{result_id}")
def update_result(
    result_id: int,
    result: ResultUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ Allow only admin or teacher
    if current_user.role not in [RoleEnum.admin, RoleEnum.teacher]:
        raise HTTPException(
            status_code=403, detail="Only teachers or admins can update results"
        )

    # ✅ If teacher, check permission
    if current_user.role == RoleEnum.teacher:
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=403, detail="Teacher profile not found")

        # Get existing result to know which student & subject it is for
        db_result = db.query(Result).filter(Result.id == result_id).first()
        if not db_result:
            raise HTTPException(status_code=404, detail="Result not found")

        # Get student to find class
        student = db.query(Student).filter(Student.id == db_result.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Check permission: teacher must be assigned to this subject & class
        link = (
            db.query(ClassSubjectTeacher)
            .filter(
                ClassSubjectTeacher.class_id == student.class_id,
                ClassSubjectTeacher.subject_id == db_result.subject_id,
                ClassSubjectTeacher.teacher_id == teacher.id,
            )
            .first()
        )

        if not link:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to teach this subject in this class",
            )

    # ✅ If admin OR verified teacher, allow update
    return ur(db, result_id, result)


@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete results")
    return dr(db, result_id)
