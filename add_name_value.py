from app.database import SessionLocal
from app import models

db = SessionLocal()

users = db.query(models.User).all()

for user in users:
    # Example: use email prefix as name
    user.name = user.email.split("@")[0].replace(".", " ").title()

db.commit()
db.close()

print("Names added to existing users!")
