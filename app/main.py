# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings  # ✅ updated import

from app.core.database import Base, engine, TenantScopedSession
from app.api.routes import (
    auth,
    students,
    teachers,
    classes,
    subjects,
    results,
    reports as reports_router,
    class_subject_teacher,
    academic_years,
    attendance,
)
from dotenv import load_dotenv
from app.middleware.tenant import TenantMiddleware
from starlette.requests import Request

load_dotenv()

# Load allowed origins from settings (comma-separated list)
ALLOWED_ORIGINS = [
    origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()
]

print(f"Allowed origins: {ALLOWED_ORIGINS}")  # Debugging line to check allowed origins

# Instantiate FastAPI app
app = FastAPI(
    title="Skolanova API",
    version="1.0.0",
)

# Add middleware before any routers
app.add_middleware(TenantMiddleware)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    tenant_id = None
    if hasattr(request.state, "tenant") and request.state.tenant:
        tenant_id = request.state.tenant.id

    request.state.db = TenantScopedSession(
        tenant_id=tenant_id, bind=engine, autoflush=False, autocommit=False
    )
    try:
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


# ✅ CORS Middleware (put real origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables (for local dev only; Alembic in prod)
if settings.ENVIRONMENT == "dev":
    Base.metadata.create_all(bind=engine)

# ✅ Include routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(results.router)
app.include_router(reports_router.router)
app.include_router(class_subject_teacher.router)
app.include_router(academic_years.router)
app.include_router(attendance.router)
