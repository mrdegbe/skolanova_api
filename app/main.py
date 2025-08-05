# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings  # ✅ updated import

from app.core.database import Base, engine  # ✅ Use your new core.database
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

load_dotenv()

# Load allowed origins from settings (comma-separated list)
ALLOWED_ORIGINS = [
    origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()
]

# Instantiate FastAPI app
app = FastAPI(
    title="Skolanova API",
    version="1.0.0",
)

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
