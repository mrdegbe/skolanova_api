from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas


def create_class(db: Session, _class: schemas.ClassCreate):
    db_class = models.Class(**_class.model_dump())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def get_classes(db: Session, skip: int = 0, limit: int = 100):
    classes = db.query(models.Class).offset(skip).limit(limit).all()

    results = []
    for cls in classes:
        result = {
            "id": cls.id,
            "name": cls.name,
            "class_teacher_id": cls.class_teacher_id,
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
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()

    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    result = {
        "id": class_.id,
        "name": class_.name,
        "class_teacher_id": class_.class_teacher_id,
        "class_teacher_name": None,
        "created_at": class_.created_at,
        "updated_at": class_.updated_at,
    }

    if class_.class_teacher:
        result["class_teacher_name"] = (
            f"{class_.class_teacher.first_name} {class_.class_teacher.last_name}"
        )

    return result


def update_class(db: Session, class_id: int, _class: schemas.ClassUpdate):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not db_class:
        raise Exception("Class not found")

    if _class.name is not None:
        db_class.name = _class.name

    if _class.class_teacher_id is not None:
        db_class.class_teacher_id = _class.class_teacher_id

    db.commit()
    db.refresh(db_class)
    return db_class


def delete_class(db: Session, class_id: int):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not db_class:
        raise Exception("Class not found")
    db.delete(db_class)
    db.commit()
    return {"ok": True}
