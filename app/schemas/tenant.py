from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class TenantBase(BaseModel):
    name: str
    slug: str
    school_logo: Optional[str] = None


class TenantCreate(TenantBase):
    pass


class TenantOut(TenantBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}
