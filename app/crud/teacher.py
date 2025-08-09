# app/crud/teacher.py

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import hash_password
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.models.user import User, RoleEnum
from app.models.class_subject_teacher import ClassSubjectTeacher


def create_teacher(db: Session, teacher_data: TeacherCreate, tenant_id: int):
    try:
        # TODO: generate a secure random password for production
        password = "password"
        password_hash = hash_password(password)

        # Create linked User with tenant_id
        db_user = User(
            email=teacher_data.email,
            password_hash=password_hash,
            role=RoleEnum.teacher,
            name=f"{teacher_data.first_name} {teacher_data.last_name}",
            tenant_id=tenant_id,
        )
        db.add(db_user)

        # Create Teacher with tenant_id
        db_teacher = Teacher(
            first_name=teacher_data.first_name,
            last_name=teacher_data.last_name,
            gender=teacher_data.gender,
            address=teacher_data.address,
            user_id=None,  # will link after flush
            contact=teacher_data.contact,
            status=teacher_data.status,
            specialization=teacher_data.specialization,
            tenant_id=tenant_id,
        )
        db.add(db_teacher)

        db.flush()  # get generated IDs
        db_teacher.user_id = db_user.id

        # create assignment links
        for assignment in teacher_data.assignments or []:
            for subject_id in assignment.subject_ids:
                link = ClassSubjectTeacher(
                    class_id=assignment.class_id,
                    subject_id=subject_id,
                    teacher_id=db_teacher.id,
                    tenant_id=tenant_id,
                )
                db.add(link)

        db.commit()
        db.refresh(db_teacher)
        db.refresh(db_user)

        return {
            "teacher": {
                "name": f"{db_teacher.first_name} {db_teacher.last_name}",
                "email": db_user.email,
            },
            "plain_password": password,
        }

    except SQLAlchemyError:
        db.rollback()
        raise


def update_teacher(
    db: Session, teacher_id: int, update_data: TeacherUpdate, tenant_id: int
):
    db_teacher = (
        db.query(Teacher)
        .filter(Teacher.id == teacher_id, Teacher.tenant_id == tenant_id)
        .first()
    )
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # update fields
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

    # wipe & recreate assignments if provided
    if update_data.assignments is not None:
        db.query(ClassSubjectTeacher).filter(
            ClassSubjectTeacher.teacher_id == teacher_id,
            ClassSubjectTeacher.tenant_id == tenant_id,
        ).delete()

        for assignment in update_data.assignments:
            for subject_id in assignment.subject_ids:
                link = ClassSubjectTeacher(
                    teacher_id=teacher_id,
                    class_id=assignment.class_id,
                    subject_id=subject_id,
                    tenant_id=tenant_id,
                )
                db.add(link)

    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def get_teachers(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    teachers = (
        db.query(Teacher)
        .filter(Teacher.tenant_id == tenant_id)
        .options(
            joinedload(Teacher.user),  # load user so email is available
            joinedload(Teacher.subject_links).joinedload(ClassSubjectTeacher.class_),
            joinedload(Teacher.subject_links).joinedload(ClassSubjectTeacher.subject),
            joinedload(Teacher.homeroom_classes),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for teacher in teachers:
        subject_links = [
            {
                "id": link.id,
                "class_id": link.class_id,
                "class_name": link.class_.name if link.class_ else None,
                "subject_id": link.subject_id,
                "subject_name": link.subject.name if link.subject else None,
                "teacher_id": link.teacher_id,
            }
            for link in teacher.subject_links
        ]

        homeroom_classes = [
            {"id": cls.id, "name": cls.name} for cls in teacher.homeroom_classes
        ]

        result.append(
            {
                "id": teacher.id,
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
                "gender": teacher.gender,
                "email": teacher.user.email if teacher.user else None,
                "contact": teacher.contact,
                "status": teacher.status,
                "specialization": teacher.specialization,
                "address": teacher.address,
                "homeroom_classes": homeroom_classes,
                "created_at": teacher.created_at,
                "updated_at": teacher.updated_at,
                "subject_links": subject_links,
            }
        )

    return result


def get_teacher(db: Session, teacher_id: int, tenant_id: int):
    return (
        db.query(Teacher)
        .filter(Teacher.id == teacher_id, Teacher.tenant_id == tenant_id)
        .options(joinedload(Teacher.subject_links), joinedload(Teacher.user))
        .first()
    )


def delete_teacher(db: Session, teacher_id: int, tenant_id: int):
    db_teacher = get_teacher(db, teacher_id, tenant_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"ok": True}


def get_teacher(db: Session, teacher_id: int, request: Request):
    tenant_id = request.state.tenant.id
    return (
        db.query(Teacher)
        .filter(Teacher.id == teacher_id, Teacher.tenant_id == tenant_id)
        .options(joinedload(Teacher.subject_links), joinedload(Teacher.user))
        .first()
    )


def delete_teacher(db: Session, teacher_id: int, request: Request):
    tenant_id = request.state.tenant.id
    db_teacher = get_teacher(db, teacher_id, request)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"ok": True}
