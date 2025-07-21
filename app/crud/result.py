from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.result import Result
from app.schemas.result import ResultBase, ResultCreate, ResultOut, ResultUpdate


def create_result(db: Session, result: ResultCreate):
    db_result = Result(**result.model_dump())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Result).offset(skip).limit(limit).all()


def get_result(db: Session, result_id: int):
    return db.query(Result).filter(Result.id == result_id).first()


def update_result(db: Session, result_id: int, result: ResultCreate):
    db_result = get_result(db, result_id)
    if not db_result:
        raise Exception("Result not found")

    # ✅ Only allow changing the score — nothing else!
    db_result.score = result.score

    db.commit()
    db.refresh(db_result)
    return db_result


def delete_result(db: Session, result_id: int):
    db_result = get_result(db, result_id)
    if not db_result:
        raise Exception("Result not found")
    db.delete(db_result)
    db.commit()
    return {"ok": True}
