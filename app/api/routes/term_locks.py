from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

# from app.core import deps
from app.core.dependencies import get_current_tenant, get_db
from app.models.tenant import Tenant
from app.schemas.term_lock import TermLockCreate, TermLockOut
from app.crud import term_lock as crud_term_lock

# router = APIRouter()
router = APIRouter(
    prefix="/terms",
    tags=["TermLock"],
)


@router.post("/lock", response_model=TermLockOut)
def lock_term_endpoint(
    data: TermLockCreate,
    db: Session = Depends(get_db),
    # tenant: Tenant = Depends(get_current_tenant),
):
    try:
        term_lock = crud_term_lock.create_term_lock(db=db, data=data)
        return term_lock
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.post("/lock", response_model=TermLockOut)
# def lock_term(data: TermLockCreate, db: Session = Depends(get_db)):
#     return crud_term_lock.create_term_lock(db, data)
