# Run this in a script or shell
from app.database import SessionLocal
from app import models, auth

db = SessionLocal()

hashed = auth.hash_password("teacher")
user = models.User(
    email="teacher@example.com", password_hash=hashed, role=models.RoleEnum.teacher
)
db.add(user)
db.commit()
db.refresh(user)

teacher = models.Teacher(first_name="Mary", last_name="Johnson", user_id=user.id)
db.add(teacher)
db.commit()
db.refresh(teacher)

print("Teacher created:", teacher)

db.close()
