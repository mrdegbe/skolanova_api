from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import GenderEnum, FeeStatusEnum
from sqlalchemy.dialects.postgresql import UUID


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime(timezone=True))
    gender = Column(
        Enum(
            GenderEnum,
            name="genderenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    fee_status = Column(
        Enum(
            FeeStatusEnum,
            name="feestatusenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    guardian_name = Column(String)
    guardian_contact = Column(String)
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,  # Set to False after backfilling
        index=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("classes.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    address = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    # ✅ Relationships
    class_ = relationship("Class", back_populates="students")
    results = relationship("Result", back_populates="student")
    tenant = relationship("Tenant", back_populates="students")

    def __repr__(self):
        return f"<Student id={self.id} name={self.first_name} {self.last_name}>"

    def __str__(self):
        return self.__repr__()
