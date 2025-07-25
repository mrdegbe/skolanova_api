"""Updated string data type to enum

Revision ID: 99d174158d2a
Revises: 4376c1161162
Create Date: 2025-07-25 02:06:23.165430
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import enum

# revision identifiers, used by Alembic.
revision: str = '99d174158d2a'
down_revision: Union[str, Sequence[str], None] = '4376c1161162'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ✅ Exact-casing Enums to match your actual values in DB
class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class TeacherStatusEnum(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ON_LEAVE = "On Leave"

class FeeStatusEnum(str, enum.Enum):
    PAID = "Paid"
    UNPAID = "Unpaid"
    PARTIAL = "Partial"

def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()

    # ✅ 0️⃣ Drop conflicting existing enums first
    op.execute("DROP TYPE IF EXISTS genderenum CASCADE;")
    op.execute("DROP TYPE IF EXISTS teacherstatusenum CASCADE;")
    op.execute("DROP TYPE IF EXISTS feestatusenum CASCADE;")

    # ✅ 1️⃣ Create new enums with PascalCase values
    gender_enum = sa.Enum(
        GenderEnum,
        name="genderenum",
        values_callable=lambda enum_cls: [e.value for e in enum_cls]
    )
    gender_enum.create(bind, checkfirst=True)

    teacher_status_enum = sa.Enum(
        TeacherStatusEnum,
        name="teacherstatusenum",
        values_callable=lambda enum_cls: [e.value for e in enum_cls]
    )
    teacher_status_enum.create(bind, checkfirst=True)

    fee_status_enum = sa.Enum(
        FeeStatusEnum,
        name="feestatusenum",
        values_callable=lambda enum_cls: [e.value for e in enum_cls]
    )
    fee_status_enum.create(bind, checkfirst=True)

    # ✅ 2️⃣ Normalize casing in existing rows just in case
    op.execute("UPDATE students SET gender = 'Male' WHERE gender ILIKE 'male';")
    op.execute("UPDATE students SET gender = 'Female' WHERE gender ILIKE 'female';")
    op.execute("UPDATE students SET gender = 'Other' WHERE gender ILIKE 'other';")

    op.execute("UPDATE teachers SET gender = 'Male' WHERE gender ILIKE 'male';")
    op.execute("UPDATE teachers SET gender = 'Female' WHERE gender ILIKE 'female';")
    op.execute("UPDATE teachers SET gender = 'Other' WHERE gender ILIKE 'other';")

    op.execute("UPDATE students SET fee_status = 'Paid' WHERE fee_status ILIKE 'paid';")
    op.execute("UPDATE students SET fee_status = 'Unpaid' WHERE fee_status ILIKE 'unpaid';")
    op.execute("UPDATE students SET fee_status = 'Partial' WHERE fee_status ILIKE 'partial';")

    op.execute("UPDATE teachers SET status = 'Active' WHERE status ILIKE 'active';")
    op.execute("UPDATE teachers SET status = 'Inactive' WHERE status ILIKE 'inactive';")
    op.execute("UPDATE teachers SET status = 'On Leave' WHERE status ILIKE 'on leave';")

    # ✅ 3️⃣ Apply the type changes
    op.execute("""
        ALTER TABLE students
        ALTER COLUMN gender TYPE genderenum
        USING gender::genderenum
    """)

    op.execute("""
        ALTER TABLE students
        ALTER COLUMN fee_status TYPE feestatusenum
        USING fee_status::feestatusenum
    """)

    op.execute("""
        ALTER TABLE teachers
        ALTER COLUMN gender TYPE genderenum
        USING gender::genderenum
    """)

    op.execute("""
        ALTER TABLE teachers
        ALTER COLUMN status TYPE teacherstatusenum
        USING status::teacherstatusenum
    """)

def downgrade() -> None:
    """Downgrade schema."""

    bind = op.get_bind()

    op.execute("""
        ALTER TABLE teachers
        ALTER COLUMN status TYPE VARCHAR
    """)
    op.execute("""
        ALTER TABLE teachers
        ALTER COLUMN gender TYPE VARCHAR
    """)
    op.execute("""
        ALTER TABLE students
        ALTER COLUMN fee_status TYPE VARCHAR
    """)
    op.execute("""
        ALTER TABLE students
        ALTER COLUMN gender TYPE VARCHAR
    """)

    sa.Enum(name="teacherstatusenum").drop(bind, checkfirst=True)
    sa.Enum(name="genderenum").drop(bind, checkfirst=True)
    sa.Enum(name="feestatusenum").drop(bind, checkfirst=True)
