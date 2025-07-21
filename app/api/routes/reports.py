# app/routers/reports.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.crud.reports import generate_student_report_pdf

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/student/{student_id}/pdf")
def get_student_report(
    student_id: int,
    term: str,
    year_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generates PDF report for a student for given term (as string) and year (int).
    """
    try:
        pdf_buffer = generate_student_report_pdf(db, student_id, term, year_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=report_{student_id}.pdf"},
    )
