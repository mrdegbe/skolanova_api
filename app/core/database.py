# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings  # ✅ get DATABASE_URL safely
from sqlalchemy.inspection import inspect

# Use DATABASE_URL from validated config
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


class TenantScopedSession(Session):
    def __init__(self, tenant_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tenant_id = tenant_id

    def query(self, *entities, **kwargs):
        query = super().query(*entities, **kwargs)
        if self._tenant_id:
            for entity in entities:
                try:
                    mapper = inspect(entity)
                    if "tenant_id" in mapper.columns:
                        query = query.filter(
                            mapper.columns["tenant_id"] == self._tenant_id
                        )
                except Exception:
                    pass
        return query


def get_tenant_scoped_session(tenant_id=None):
    return sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=TenantScopedSession
    )(tenant_id=tenant_id)


from app.models.tenant import Tenant  # adjust path if different


def get_tenant_by_slug(db: Session, slug: str):
    return db.query(Tenant).filter(Tenant.slug == slug).first()


# class TenantScopedSession(Session):
#     def __init__(self, tenant_id=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._tenant_id = tenant_id

#     def query(self, *entities, **kwargs):
#         query = super().query(*entities, **kwargs)
#         if self._tenant_id:
#             for entity in entities:
#                 try:
#                     mapper = inspect(entity)
#                     if "tenant_id" in mapper.columns:
#                         query = query.filter(
#                             mapper.columns["tenant_id"] == self._tenant_id
#                         )
#                 except Exception:
#                     pass
#         return query


# Instead of a plain SessionLocal, we use this factory
# def get_tenant_scoped_session(tenant_id=None):
#     return sessionmaker(
#         autocommit=False, autoflush=False, bind=engine, class_=TenantScopedSession
#     )(tenant_id=tenant_id)
