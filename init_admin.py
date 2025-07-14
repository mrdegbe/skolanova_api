# init_admin.py

from app.database import SessionLocal
from app import models, auth

db = SessionLocal()

hashed = auth.hash_password("admin")
admin = models.User(
    email="mrdegbe@example.com", password_hash=hashed, role=models.RoleEnum.admin, name="Raymond Degbe"
)
db.add(admin)
db.commit()

print("Admin created.")
db.close()
