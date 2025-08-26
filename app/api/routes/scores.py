from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.core.database import get_db
from app.schemas.score import ScoreCreate, ScoreCreatePayload, ScoreOut
from app.crud.score import (
    create_score,
    update_score,
    get_scores_by_class_term_subject_year,
)

# Multi-tenant dependency (you’ll need to implement get_tenant_id)
from app.core.dependencies import get_current_tenant, get_db


router = APIRouter(
    prefix="/scores",
    tags=["scores"],
)


@router.post("/", response_model=List[ScoreOut])
def save_draft(
    payload: ScoreCreatePayload,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
):
    """
    Save a draft score (not yet finalized).
    """
    return create_score(db=db, obj_in=payload, tenant_id=tenant.id)


@router.post("/submit", response_model=ScoreOut)
def submit_scores(
    payload: ScoreCreate,
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
):
    """
    Submit/finalize scores. Locks them for editing.
    """
    score = create_score(db=db, obj_in=payload, tenant_id=tenant.id)
    # TODO: update status to "submitted" after creation
    return score
