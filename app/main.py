# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
)

# ✅ Create all tables — in prod you'd do this with Alembic, not at runtime
Base.metadata.create_all(bind=engine)

# ✅ Instantiate FastAPI app
app = FastAPI(
    title="Your School Management API",
    version="1.0.0",
)

# ✅ CORS Middleware (put real origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],  # Replace with allowed origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
