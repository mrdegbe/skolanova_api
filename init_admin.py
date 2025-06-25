# init_admin.py

from app.database import SessionLocal
from app import models, auth

db = SessionLocal()

hashed = auth.hash_password("admin")
admin = models.User(
    email="admin@example.com", password_hash=hashed, role=models.RoleEnum.admin
)
db.add(admin)
db.commit()

print("Admin created.")
db.close()
