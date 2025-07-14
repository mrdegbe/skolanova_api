from sqlalchemy.orm import Session, joinedload
from .. import models, auth, schemas
import secrets, string


def create_class(db: Session, _class: schemas.ClassCreate):
    db_class = models.Class(**_class.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Class).offset(skip).limit(limit).all()


def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()


def update_class(db: Session, class_id: int, _class: schemas.ClassCreate):
    db_class = get_class(db, class_id)
    if not db_class:
        raise Exception("Class not found")
    for key, value in _class.dict().items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class


def delete_class(db: Session, class_id: int):
    db_class = get_class(db, class_id)
    if not db_class:
        raise Exception("Class not found")
    db.delete(db_class)
    db.commit()
    return {"ok": True}
