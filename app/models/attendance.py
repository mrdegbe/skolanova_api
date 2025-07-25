from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Date,
    String,
    Enum,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

from app.models.enums import AttendanceStatusEnum


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    academic_year_id = Column(
        Integer,
        ForeignKey("academic_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False, index=True)

    status = Column(
        Enum(
            AttendanceStatusEnum,
            name="attendancestatusenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    marked_by = Column(
        Integer,
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    remark = Column(String)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("student_id", "date", name="uq_attendance_student_date"),
    )

    student = relationship("Student")
    class_ = relationship("Class")
    academic_year = relationship("AcademicYear")
    teacher = relationship("Teacher")

    def __repr__(self):
        return f"<Attendance id={self.id} student_id={self.student_id} date={self.date} status={self.status}>"

    def __str__(self):
        return self.__repr__()
