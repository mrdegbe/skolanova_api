# FastAPI app instance

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import SessionLocal, engine, Base
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    students,
    teachers,
    classes,
    subjects,
    results,
    reports as reports_router,
    config as config_router,
    class_subject_teacher,
)


Base.metadata.create_all(bind=engine)

app = FastAPI()

# 👉 Add CORS middleware **immediately**
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(results.router)
app.include_router(reports_router.router)
app.include_router(config_router.router)
app.include_router(class_subject_teacher.router)


@app.post("/auth/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # fake_name = user.email.split("@")[0].replace(".", " ").title()
    # ✅ Build the payload with email and role too:
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": str(user.role.value),  # if you store it as Enum, convert to string
        "name": user.name,
    }

    access_token = auth.create_access_token(data=token_data)  # {"sub": str(user.id)}
    return {"access_token": access_token, "token_type": "bearer"}
