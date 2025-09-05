# app/crud/term_lock.py
# from sqlalchemy.orm import Session
# from app.models.term_lock import TermLock
# from app.schemas.term_lock import TermLockCreate
# from sqlalchemy.exc import IntegrityError


# def lock_term(db: Session, data: TermLockCreate, tenant_id):
#     """
#     Lock a term for a specific academic year and class.
#     If it already exists, update it. Otherwise, create a new lock.
#     """

#     term_lock = (
#         db.query(TermLock)
#         .filter(
#             TermLock.academic_year_id == data.academic_year_id,
#             TermLock.class_id == data.class_id,
#             TermLock.term == data.term,
#             TermLock.tenant_id == tenant_id,
#         )
#         .first()
#     )

#     if term_lock:
#         # Update existing lock
#         term_lock.is_locked = True
#     else:
#         # Create new term lock
#         term_lock = TermLock(
#             academic_year_id=data.academic_year_id,
#             class_id=data.class_id,
#             term=data.term,
#             is_locked=True,
#             tenant_id=tenant_id,
#         )
#         db.add(term_lock)

#     try:
#         db.commit()
#         db.refresh(term_lock)
#         return term_lock
#     except IntegrityError:
#         db.rollback()
#         raise

from sqlalchemy.orm import Session
from app.models import TermLock, AcademicYear
from app.models.tenant import Tenant
from app.schemas.term_lock import TermLockCreate
from fastapi import HTTPException


# def create_term_lock(db: Session, data: TermLockCreate):
#     # Get active academic year
#     academic_year = db.query(AcademicYear).filter(AcademicYear.is_active == True).first()
#     if not academic_year:
#         raise HTTPException(status_code=400, detail="No active academic year found")

#     # Check if already locked
#     existing = (
#         db.query(TermLock)
#         .filter(
#             TermLock.class_id == data.class_id,
#             TermLock.term == data.term,
#             TermLock.academic_year_id == academic_year.id,
#             TermLock.tenant_id == data.tenant_id,
#         )
#         .first()
#     )
#     if existing:
#         raise HTTPException(status_code=400, detail="This term is already locked")

#     term_lock = TermLock(
#         class_id=data.class_id,
#         term=data.term,
#         tenant_id=data.tenant_id,
#         academic_year_id=academic_year.id,
#         is_locked=True,
#     )
#     db.add(term_lock)
#     db.commit()
#     db.refresh(term_lock)
#     return term_lock


def create_term_lock(db: Session, data: TermLockCreate):
    print("Creating term lock for tenant slug:", data.slug)
    # 1. Get tenant by slug
    tenant = db.query(Tenant).filter(Tenant.slug == data.slug).first()
    if not tenant:
        raise HTTPException(
            status_code=404, detail=f"Tenant with slug '{data.slug}' not found"
        )

    # 2. Get active academic year for this tenant
    academic_year = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.is_active == True,
            AcademicYear.tenant_id == tenant.id,
        )
        .first()
    )
    if not academic_year:
        raise HTTPException(
            status_code=400, detail="No active academic year found for this tenant"
        )

    # 3. Check if already locked
    existing = (
        db.query(TermLock)
        .filter(
            TermLock.class_id == data.class_id,
            TermLock.term == data.term,
            TermLock.academic_year_id == academic_year.id,
            TermLock.tenant_id == tenant.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="This term is already locked")

    # 4. Create lock
    term_lock = TermLock(
        class_id=data.class_id,
        term=data.term,
        tenant_id=tenant.id,
        academic_year_id=academic_year.id,
        is_locked=True,
    )
    db.add(term_lock)
    db.commit()
    db.refresh(term_lock)
    return term_lock
