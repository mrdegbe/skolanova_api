# init_admin.py

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.enums import RoleEnum
from app.models.tenant import Tenant  # ✅ to fetch tenant
import uuid

db = SessionLocal()

# 1️⃣ Find the tenant
tenant = db.query(Tenant).filter(Tenant.slug == "futurestars").first()
if not tenant:
    raise ValueError("Tenant 'futurestars' not found in the database.")

# 2️⃣ Hash the password
hashed = hash_password("admin")  # change password if needed

# 3️⃣ Create admin linked to this tenant
admin = User(
    email="futureadmin@skolanova.org",
    password_hash=hashed,
    role=RoleEnum.admin,
    name="Futurestars Admin",
    tenant_id=tenant.id  # ✅ link to tenant
)

# 4️⃣ Save to DB
db.add(admin)
db.commit()

print(f"Admin for 'futurestars' created with email {admin.email}")
db.close()


# init_admin.py

# from app.core.database import SessionLocal
# # from app.api.routes import auth
# from app.core.security import hash_password  # Ensure you have the correct import path
# from app.models.user import User  # Ensure you have the correct import path
# from app.models.enums import RoleEnum  # Import your RoleEnum if needed

# db = SessionLocal()

# hashed = hash_password("admin")
# admin = User(
#     email="mrdegbe@skolanova.org", password_hash=hashed, role=RoleEnum.admin, name="Raymond Degbe"
# )
# db.add(admin)
# db.commit()

# print("Admin created.")
# db.close()
