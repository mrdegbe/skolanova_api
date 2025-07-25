from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.class_ import Class
from app.schemas.class_ import ClassCreate, ClassBase, ClassOut, ClassUpdate


def create_class(db: Session, class_: ClassCreate):
    db_class = Class(**class_.model_dump())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def get_classes(db: Session, skip: int = 0, limit: int = 100):
    classes = (
        db.query(Class)
        .options(
            joinedload(Class.academic_year)
        )  # 👈 Make sure related academic_year is loaded!
        .options(joinedload(Class.class_teacher))  # 👈 Same for class_teacher if needed
        .offset(skip)
        .limit(limit)
        .all()
    )

    results = []
    for cls in classes:
        result = {
            "id": cls.id,
            "name": cls.name,
            "class_teacher_id": cls.class_teacher_id,
            "academic_year_id": cls.academic_year_id,
            "academic_year_id": cls.academic_year.id if cls.academic_year else None,
            "academic_year_name": cls.academic_year.name if cls.academic_year else None,
            "class_teacher_name": None,
            "created_at": cls.created_at,
            "updated_at": cls.updated_at,
        }

        if cls.class_teacher:
            result["class_teacher_name"] = (
                f"{cls.class_teacher.first_name} {cls.class_teacher.last_name}"
            )

        results.append(result)

    return results


def get_class(db: Session, class_id: int):
    class_ = (
        db.query(Class)
        .options(joinedload(Class.academic_year), joinedload(Class.class_teacher))
        .filter(Class.id == class_id)
        .first()
    )

    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    result = {
        "id": class_.id,
        "name": class_.name,
        "class_teacher_id": class_.class_teacher_id,
        "academic_year_id": class_.academic_year_id,
        "academic_year": None,  # 👈 add this
        "class_teacher_name": None,
        "created_at": class_.created_at,
        "updated_at": class_.updated_at,
    }

    if class_.academic_year:
        result["academic_year"] = {
            "id": class_.academic_year.id,
            "name": class_.academic_year.name,
        }

    if class_.class_teacher:
        result["class_teacher_name"] = (
            f"{class_.class_teacher.first_name} {class_.class_teacher.last_name}"
        )

    return result


def update_class(db: Session, class_id: int, class_: ClassUpdate):
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if not db_class:
        raise Exception("Class not found")

    if class_.name is not None:
        db_class.name = class_.name

    if class_.class_teacher_id is not None:
        db_class.class_teacher_id = class_.class_teacher_id

    if class_.academic_year_id is not None:  # ✅ ADD THIS
        db_class.academic_year_id = class_.academic_year_id

    db.commit()
    db.refresh(db_class)
    return db_class


def delete_class(db: Session, class_id: int):
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if not db_class:
        raise Exception("Class not found")
    db.delete(db_class)
    db.commit()
    return {"ok": True}
