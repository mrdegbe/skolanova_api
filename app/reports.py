# app/reports.py
# PDF/Excel generation logic

from sqlalchemy.orm import Session
from app import models
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_student_report_pdf(
    db: Session, student_id: int, term: str, year_id: int
):
    # Convert string to TermEnum
    try:
        term_enum = models.TermEnum(term)
    except ValueError:
        raise Exception(f"Invalid term: {term}")

    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise Exception("Student not found")

    # Get all results for this term & year
    results = (
        db.query(models.Result)
        .filter(
            models.Result.student_id == student_id,
            models.Result.term == term_enum,
            models.Result.year_id == year_id,
        )
        .all()
    )

    if not results:
        raise Exception("No results for this student in this term/year")

    # Calculate total and average
    total_score = sum(r.score for r in results)
    average_score = total_score / len(results)

    # Get all students in this class for ranking
    classmates = (
        db.query(models.Student)
        .filter(models.Student.class_id == student.class_id)
        .all()
    )
    class_scores = []
    for mate in classmates:
        mate_results = (
            db.query(models.Result)
            .filter(
                models.Result.student_id == mate.id,
                models.Result.term == term_enum,
                models.Result.year_id == year_id,
            )
            .all()
        )
        if mate_results:
            mate_total = sum(r.score for r in mate_results)
            class_scores.append((mate.id, mate_total))

    # Rank students
    class_scores.sort(key=lambda x: x[1], reverse=True)
    position = next(
        (i + 1 for i, (sid, _) in enumerate(class_scores) if sid == student_id), None
    )

    # Generate PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, f"Terminal Report")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Name: {student.first_name} {student.last_name}")
    p.drawString(50, height - 120, f"Class: {student.class_.name}")
    p.drawString(50, height - 140, f"Term: {term_enum.value}  |  Year: {year_id}")

    y = height - 180
    p.drawString(50, y, "Subject")
    p.drawString(300, y, "Score")
    y -= 20

    for r in results:
        p.drawString(50, y, r.subject.name)
        p.drawString(300, y, str(r.score))
        y -= 20

    y -= 10
    p.drawString(50, y, f"Total: {total_score}")
    y -= 20
    p.drawString(50, y, f"Average: {average_score:.2f}")
    y -= 20
    p.drawString(50, y, f"Position in class: {position} of {len(class_scores)}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
