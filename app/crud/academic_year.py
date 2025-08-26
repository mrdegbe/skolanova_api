from sqlalchemy.orm import Session
from app.models.academic_year import AcademicYear as AcademicYearModel
from app.schemas.academic_year import AcademicYearCreate


def create_academic_year(db: Session, ay: AcademicYearCreate, tenant_id: int):
    if ay.is_active:
        db.query(AcademicYearModel).filter(
            AcademicYearModel.tenant_id == tenant_id
        ).update({AcademicYearModel.is_active: False})

    db_ay = AcademicYearModel(**ay.model_dump(), tenant_id=tenant_id)
    db.add(db_ay)
    db.commit()
    db.refresh(db_ay)
    return db_ay


def get_academic_years(db: Session, tenant_id: int):
    return (
        db.query(AcademicYearModel)
        .filter(AcademicYearModel.tenant_id == tenant_id)
        .all()
    )


def get_academic_year(db: Session, ay_id: int, tenant_id: int):
    return (
        db.query(AcademicYearModel)
        .filter(AcademicYearModel.id == ay_id, AcademicYearModel.tenant_id == tenant_id)
        .first()
    )


def update_academic_year(
    db: Session, ay_id: int, ay_update: AcademicYearCreate, tenant_id: str
):
    db_ay = (
        db.query(AcademicYearModel)
        .filter(AcademicYearModel.id == ay_id, AcademicYearModel.tenant_id == tenant_id)
        .first()
    )
    if db_ay is None:
        return None

    # Only deactivate other years for the same tenant
    if ay_update.is_active:
        db.query(AcademicYearModel).filter(
            AcademicYearModel.tenant_id == tenant_id, AcademicYearModel.id != ay_id
        ).update({AcademicYearModel.is_active: False})

    # Update fields
    for key, value in ay_update.model_dump().items():
        setattr(db_ay, key, value)

    db.commit()
    db.refresh(db_ay)
    return db_ay


# def update_academic_year(
#     db: Session, ay_id: int, ay_update: AcademicYearCreate, tenant_id: int
# ):
#     db_ay = (
#         db.query(AcademicYearModel)
#         .filter(AcademicYearModel.id == ay_id, AcademicYearModel.tenant_id == tenant_id)
#         .first()
#     )
#     if db_ay is None:
#         return None

#     if ay_update.is_active:
#         db.query(AcademicYearModel).filter(
#             AcademicYearModel.tenant_id == tenant_id
#         ).update({AcademicYearModel.is_active: False})

#     for key, value in ay_update.model_dump().items():
#         setattr(db_ay, key, value)
#     db.commit()
#     db.refresh(db_ay)
#     return db_ay


def delete_academic_year(db: Session, ay_id: int, tenant_id: int):
    db_ay = (
        db.query(AcademicYearModel)
        .filter(AcademicYearModel.id == ay_id, AcademicYearModel.tenant_id == tenant_id)
        .first()
    )
    if db_ay is None:
        return None
    db.delete(db_ay)
    db.commit()
    return db_ay
