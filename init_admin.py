# init_admin.py

from app.core.database import SessionLocal
# from app.api.routes import auth
from app.core.security import hash_password  # Ensure you have the correct import path
from app.models.user import User  # Ensure you have the correct import path
from app.models.enums import RoleEnum  # Import your RoleEnum if needed

db = SessionLocal()

hashed = hash_password("admin")
admin = User(
    email="mrdegbe@skolanova.org", password_hash=hashed, role=RoleEnum.admin, name="Raymond Degbe"
)
db.add(admin)
db.commit()

print("Admin created.")
db.close()
