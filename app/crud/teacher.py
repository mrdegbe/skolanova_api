from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import secrets, string

from app.core.security import hash_password, verify_password, create_access_token
from app.models.teacher import Teacher
from app.schemas.teacher import (
    TeacherBase,
    TeacherCreate,
    TeacherOut,
    TeacherResponse,
    TeacherUpdate,
)
from app.models.user import User, RoleEnum
from app.models.class_subject_teacher import ClassSubjectTeacher


def create_teacher(db: Session, teacher_data: TeacherCreate):

    # 1. Generate random password
    password = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(12)
    )

    # 2. Hash it
    password_hash = hash_password(password)

    # 3. Create linked User
    db_user = User(
        email=teacher_data.email,
        password_hash=password_hash,
        role=RoleEnum.teacher,
        name=f"{teacher_data.first_name} {teacher_data.last_name}",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 4. Create teacher
    db_teacher = Teacher(
        first_name=teacher_data.first_name,
        last_name=teacher_data.last_name,
        user_id=db_user.id,
        contact=teacher_data.contact,
        status=teacher_data.status,
        specialization=teacher_data.specialization,
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)

    # 6 For each assignment, create links
    for assignment in teacher_data.assignments or []:
        for subject_id in assignment.subject_ids:
            link = ClassSubjectTeacher(
                class_id=assignment.class_id,
                subject_id=subject_id,
                teacher_id=db_teacher.id,
            )
            db.add(link)
    db.commit()

    # 7. Return teacher + plain password so admin can copy
    return {
        "teacher": {
            "name": f"{db_teacher.first_name} {db_teacher.last_name}",
            "email": db_user.email,
        },
        "plain_password": password,
    }


def update_teacher(db: Session, teacher_id: int, update_data: TeacherUpdate):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Update basic fields if provided
    if update_data.first_name is not None:
        db_teacher.first_name = update_data.first_name
    if update_data.last_name is not None:
        db_teacher.last_name = update_data.last_name
    if update_data.contact is not None:
        db_teacher.contact = update_data.contact
    if update_data.status is not None:
        db_teacher.status = update_data.status
    if update_data.specialization is not None:
        db_teacher.specialization = update_data.specialization
    if update_data.gender is not None:
        db_teacher.gender = update_data.gender
    if update_data.address is not None:
        db_teacher.address = update_data.address

    # ✅ Wipe & recreate assignments if provided
    if update_data.assignments is not None:

        # Delete old links
        db.query(ClassSubjectTeacher).filter(
            ClassSubjectTeacher.teacher_id == teacher_id
        ).delete()

        # Add new links
        for assignment in update_data.assignments:
            for subject_id in assignment.subject_ids:
                link = ClassSubjectTeacher(
                    teacher_id=teacher_id,
                    class_id=assignment.class_id,
                    subject_id=subject_id,
                )
                db.add(link)

    db.commit()
    db.refresh(db_teacher)

    return db_teacher


def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Teacher)
        .options(joinedload(Teacher.subject_links), joinedload(Teacher.user))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_teacher(db: Session, teacher_id: int):
    return (
        db.query(Teacher)
        .options(joinedload(Teacher.subject_links))
        .filter(Teacher.id == teacher_id)
        .first()
    )


def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if not db_teacher:
        raise Exception("Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"ok": True}
