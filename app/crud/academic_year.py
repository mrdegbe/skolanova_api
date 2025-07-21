from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas


# I believe it's same concept as Academic Year

# def create_year(db: Session, year: schemas.YearCreate):
#     db_year = models.Year(**year.model_dump())
#     db.add(db_year)
#     db.commit()
#     db.refresh(db_year)
#     return db_year


# def get_years(db: Session):
#     return db.query(models.Year).all()
