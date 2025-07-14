# Run this in a script or shell
from app.database import SessionLocal
from app import models, auth

db = SessionLocal()

hashed = auth.hash_password("dvtee")
user = models.User(
    email="dvt@example.com", password_hash=hashed, role=models.RoleEnum.teacher, name="Raymond Degbe"
)
db.add(user)
db.commit()
db.refresh(user)

teacher = models.Teacher(first_name="Raymond", last_name="Degbe", user_id=user.id, specialization="Developer", contact="+233 24 064 8409", status="On Leave")
db.add(teacher)
db.commit()
db.refresh(teacher)

print("Teacher created:", teacher)

db.close()
