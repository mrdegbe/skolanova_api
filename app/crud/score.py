from typing import List
from sqlalchemy.orm import Session
from app.models.score import Score
from app.schemas.score import ScoreCreate, ScoreCreatePayload, ScoreUpdate


def create_score(
    db: Session, obj_in: ScoreCreatePayload, tenant_id: int
) -> List[Score]:
    """Save or update draft scores for multiple students."""
    db_objs = []

    for record in obj_in.records:
        # Check if a draft already exists for this student in the same context
        existing = (
            db.query(Score)
            .filter(
                Score.student_id == record.student_id,
                Score.class_id == obj_in.class_id,
                Score.subject_id == obj_in.subject_id,
                Score.academic_year_id == obj_in.academic_year_id,
                Score.term == obj_in.term,
                Score.tenant_id == tenant_id,
            )
            .first()
        )

        if existing:
            # Update the existing draft
            existing.class_score = record.class_score
            existing.exam_score = record.exam_score
            existing.status = "Draft"
            db_objs.append(existing)
        else:
            # Create a new draft if none exists
            new_obj = Score(
                student_id=record.student_id,
                class_id=obj_in.class_id,
                subject_id=obj_in.subject_id,
                academic_year_id=obj_in.academic_year_id,
                term=obj_in.term,
                class_score=record.class_score,
                exam_score=record.exam_score,
                tenant_id=tenant_id,
                status="Draft",
            )
            db.add(new_obj)
            db_objs.append(new_obj)

    db.commit()
    for obj in db_objs:
        db.refresh(obj)

    return db_objs


def update_score(db: Session, score_id: int, obj_in: ScoreUpdate, tenant_id: str):
    """
    Update an existing score for a tenant.
    """
    score = (
        db.query(Score)
        .filter(Score.id == score_id, Score.tenant_id == tenant_id)
        .first()
    )

    if not score:
        return None

    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(score, field, value)

    db.commit()
    db.refresh(score)
    return score


def get_scores_by_class_term_subject_year(
    db: Session,
    tenant_id: str,
    class_id: int,
    term: str,
    subject_id: int,
    academic_year_id: int,
):
    """
    Fetch scores for a class, term, subject, and academic year — restricted to tenant.
    """
    return (
        db.query(Score)
        .filter(
            Score.tenant_id == tenant_id,
            Score.class_id == class_id,
            Score.term == term,
            Score.subject_id == subject_id,
            Score.academic_year_id == academic_year_id,
        )
        .all()
    )


def get_score_by_id(db: Session, score_id: int, tenant_id: str):
    """
    Get a single score by ID — restricted to tenant.
    """
    return (
        db.query(Score)
        .filter(Score.id == score_id, Score.tenant_id == tenant_id)
        .first()
    )
