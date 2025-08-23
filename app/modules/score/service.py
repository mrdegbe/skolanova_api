from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Score, Student, Subject
from app.schemas.score import ScoreCreate, ScoreUpdate
from app.utils.grades import calculate_grade, calculate_remarks


def create_score(db: Session, score_data: ScoreCreate) -> Score:
    """Create a new score entry for a student in a subject."""
    # Calculate total, grade, remark
    total = score_data.class_score + score_data.exam_score
    grade = calculate_grade(total)
    remark = calculate_remarks(grade)

    score = Score(
        **score_data.dict(),
        total_score=total,
        grade=grade,
        remark=remark,
    )
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

    # Recalculate totals, grade, and remark if class/exam scores changed
    if score.class_score is not None and score.exam_score is not None:
        score.total_score = score.class_score + score.exam_score
        score.grade = calculate_grade(score.total_score)
        score.remark = calculate_remarks(score.grade)

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

    total_score = sum(s.total_score for s in scores)
    avg_score = total_score / len(scores)
    subjects = []

    for s in scores:
        subjects.append(
            {
                "subject": db.query(Subject)
                .filter(Subject.id == s.subject_id)
                .first()
                .name,
                "class_score": s.class_score,
                "exam_score": s.exam_score,
                "total": s.total_score,
                "grade": s.grade,
                "remark": s.remark,
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
