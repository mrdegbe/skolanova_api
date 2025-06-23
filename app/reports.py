# app/reports.py
# PDF/Excel generation logic

from sqlalchemy.orm import Session
from app import models
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_student_report_pdf(db: Session, student_id: int, term: str, year_id: int):
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
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # p = canvas.Canvas(buffer, pagesize=A4)
    # width, height = A4

    # Optional: add school logo
    # logo = Image('static/logo.png', width=50, height=50)
    # elements.append(logo)

    elements.append(Paragraph("<b>NEW DAWN INTELLIGENCE ACADEMY</b>", styles["Title"]))
    elements.append(Paragraph(f"Terminal Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(f"Name: {student.first_name} {student.last_name}", styles["Normal"])
    )
    elements.append(Paragraph(f"Class: {student.class_.name}", styles["Normal"]))
    elements.append(Paragraph(f"Term: {term} | Year ID: {year_id}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table data
    table_data = [["Subject", "Score"]]
    for r in results:
        table_data.append([r.subject.name, f"{r.score:.2f}"])

    table_data.append(["", ""])
    table_data.append(["Total", f"{total_score:.2f}"])
    table_data.append(["Average", f"{average_score:.2f}"])
    table_data.append(["Position", f"{position} of {len(class_scores)}"])

    t = Table(table_data, colWidths=[250, 100])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    elements.append(t)
    elements.append(Spacer(1, 36))

    elements.append(Paragraph("__________________________", styles["Normal"]))
    elements.append(Paragraph("Class Teacher's Signature", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer
