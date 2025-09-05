# from pydantic import BaseModel
# from uuid import UUID
# from datetime import datetime


# class TermLockBase(BaseModel):
#     academic_year_id: int
#     class_id: int
#     term: str


# class TermLockCreate(TermLockBase):
#     tenant_id: UUID


# class TermLockOut(TermLockBase):
#     id: int
#     is_locked: bool
#     created_at: datetime
#     updated_at: datetime
#     tenant_id: UUID

#     class Config:
#         orm_mode = True


from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TermLockBase(BaseModel):
    # academic_year_id: int
    class_id: int
    term: str


class TermLockCreate(TermLockBase):
    slug: str


class TermLockOut(TermLockBase):
    id: int
    academic_year_id: int
    is_locked: bool
    created_at: datetime
    updated_at: datetime
    tenant_id: UUID

    class Config:
        orm_mode = True
