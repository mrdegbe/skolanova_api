# test_insert.py

from app.database import SessionLocal
from app import models

db = SessionLocal()

# Create a user
user = models.User(
    email="admin@example.com", password_hash="testpassword", role=models.RoleEnum.admin
)
db.add(user)
db.commit()
db.refresh(user)
print("Created user:", user)

# Create a teacher linked to this user
teacher = models.Teacher(first_name="John", last_name="Doe", user_id=user.id)
db.add(teacher)
db.commit()
db.refresh(teacher)
print("Created teacher:", teacher)

# Create a class
_class = models.Class(name="Grade 6 A", teacher_id=teacher.id)
db.add(_class)
db.commit()
db.refresh(_class)
print("Created class:", _class)

# Create a student in that class
student = models.Student(first_name="Jane", last_name="Smith", class_id=_class.id)
db.add(student)
db.commit()
db.refresh(student)
print("Created student:", student)

db.close()
