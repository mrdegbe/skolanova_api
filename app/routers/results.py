# app/routers/results.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud, auth

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("/")
def create_result(
    result: schemas.ResultCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in [models.RoleEnum.admin, models.RoleEnum.teacher]:
        raise HTTPException(
            status_code=403, detail="Only teachers or admins can create results"
        )

    # ✅ If teacher: enforce subject permission
    if current_user.role == models.RoleEnum.teacher:
        # 1️⃣ Get Teacher profile linked to user
        teacher = (
            db.query(models.Teacher)
            .filter(models.Teacher.user_id == current_user.id)
            .first()
        )
        if not teacher:
            raise HTTPException(status_code=403, detail="Teacher profile not found")

        # 2️⃣ Get the student to find their class
        student = (
            db.query(models.Student)
            .filter(models.Student.id == result.student_id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # 3️⃣ Check ClassSubjectTeacher link
        link = (
            db.query(models.ClassSubjectTeacher)
            .filter(
                models.ClassSubjectTeacher.class_id == student.class_id,
                models.ClassSubjectTeacher.subject_id == result.subject_id,
                models.ClassSubjectTeacher.teacher_id == teacher.id,
            )
            .first()
        )

        if not link:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to teach this subject in this class",
            )

    # ✅ If admin or verified teacher, call CRUD to create
    return crud.create_result(db, result)


@router.get("/")
def get_results(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_results(db, skip, limit)


@router.get("/{result_id}")
def get_result(
    result_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_result(db, result_id)


@router.put("/{result_id}")
def update_result(
    result_id: int,
    result: schemas.ResultUpdate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # ✅ Allow only admin or teacher
    if current_user.role not in [models.RoleEnum.admin, models.RoleEnum.teacher]:
        raise HTTPException(
            status_code=403, detail="Only teachers or admins can update results"
        )

    # ✅ If teacher, check permission
    if current_user.role == models.RoleEnum.teacher:
        teacher = (
            db.query(models.Teacher)
            .filter(models.Teacher.user_id == current_user.id)
            .first()
        )
        if not teacher:
            raise HTTPException(status_code=403, detail="Teacher profile not found")

        # Get existing result to know which student & subject it is for
        db_result = (
            db.query(models.Result).filter(models.Result.id == result_id).first()
        )
        if not db_result:
            raise HTTPException(status_code=404, detail="Result not found")

        # Get student to find class
        student = (
            db.query(models.Student)
            .filter(models.Student.id == db_result.student_id)
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Check permission: teacher must be assigned to this subject & class
        link = (
            db.query(models.ClassSubjectTeacher)
            .filter(
                models.ClassSubjectTeacher.class_id == student.class_id,
                models.ClassSubjectTeacher.subject_id == db_result.subject_id,
                models.ClassSubjectTeacher.teacher_id == teacher.id,
            )
            .first()
        )

        if not link:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to teach this subject in this class",
            )

    # ✅ If admin OR verified teacher, allow update
    return crud.update_result(db, result_id, result)


@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete results")
    return crud.delete_result(db, result_id)
