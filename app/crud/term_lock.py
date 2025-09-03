# app/crud/term_lock.py
from sqlalchemy.orm import Session
from app.models.term_lock import TermLock
from app.schemas.term_lock import TermLockCreate
from sqlalchemy.exc import IntegrityError


def lock_term(db: Session, data: TermLockCreate, tenant_id):
    """
    Lock a term for a specific academic year and class.
    If it already exists, update it. Otherwise, create a new lock.
    """

    term_lock = (
        db.query(TermLock)
        .filter(
            TermLock.academic_year_id == data.academic_year_id,
            TermLock.class_id == data.class_id,
            TermLock.term == data.term,
            TermLock.tenant_id == tenant_id,
        )
        .first()
    )

    if term_lock:
        # Update existing lock
        term_lock.is_locked = True
    else:
        # Create new term lock
        term_lock = TermLock(
            academic_year_id=data.academic_year_id,
            class_id=data.class_id,
            term=data.term,
            is_locked=True,
            tenant_id=tenant_id,
        )
        db.add(term_lock)

    try:
        db.commit()
        db.refresh(term_lock)
        return term_lock
    except IntegrityError:
        db.rollback()
        raise
