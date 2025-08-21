from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Score, Student, Subject  # adjust to your actual models
from app.schemas import ScoreCreate, ScoreUpdate  # adjust to your actual schemas
from app.utils import calculate_grade, calculate_remarks


def create_score(db: Session, score_data: ScoreCreate) -> Score:
    """Create a new score entry for a student in a subject."""
    score = Score(**score_data.dict())
    db.add(score)
    db.commit()
    db.refresh(score)
    return score


def update_score(db: Session, score_id: int, score_data: ScoreUpdate) -> Score:
    """Update an existing score."""
    score = db.query(Score).filter(Score.id == score_id).first()
    if not score:
        return None
    for key, value in score_data.dict(exclude_unset=True).items():
        setattr(score, key, value)
    db.commit()
    db.refresh(score)
    return score


def get_student_scores(
    db: Session, student_id: int, term: str, academic_year: str
) -> List[Score]:
    """Get all scores for a student for a given term and academic year."""
    return (
        db.query(Score)
        .filter(
            Score.student_id == student_id,
            Score.term == term,
            Score.academic_year == academic_year,
        )
        .all()
    )


def calculate_term_report(
    db: Session, student_id: int, term: str, academic_year: str
) -> Dict:
    """
    Calculate total, average, and grades for a student's term report.
    """
    scores = get_student_scores(db, student_id, term, academic_year)
    if not scores:
        return {}

    total_score = sum(s.marks_obtained for s in scores)
    avg_score = total_score / len(scores)
    subjects = []

    for s in scores:
        grade = calculate_grade(s.marks_obtained)
        remark = calculate_remarks(grade)
        subjects.append(
            {
                "subject": db.query(Subject)
                .filter(Subject.id == s.subject_id)
                .first()
                .name,
                "score": s.marks_obtained,
                "grade": grade,
                "remark": remark,
            }
        )

    return {
        "student": db.query(Student).filter(Student.id == student_id).first().full_name,
        "term": term,
        "academic_year": academic_year,
        "total_score": total_score,
        "average_score": avg_score,
        "subjects": subjects,
    }
