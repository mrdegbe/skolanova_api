from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Date,
    Enum,
    func,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import RoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum))
    name = Column(String)  # ✅ NEW

    # ✅ Relationships
    teacher = relationship("Teacher", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"

    def __str__(self):
        return self.__repr__()
