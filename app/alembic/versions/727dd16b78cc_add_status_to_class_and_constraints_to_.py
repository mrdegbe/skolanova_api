"""Add status to class and constraints to result

Revision ID: 727dd16b78cc
Revises: f670cf776edf
Create Date: 2025-07-25 17:30:33.438750

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "727dd16b78cc"
down_revision: Union[str, Sequence[str], None] = "f670cf776edf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the enum type
# ✅ Correct enum values match your Python Enum
class_status_enum = sa.Enum("Active", "Archived", "Inactive", name="classstatusenum")


def upgrade() -> None:
    """Upgrade schema."""
    # Create ENUM type first
    bind = op.get_bind()
    class_status_enum.create(bind, checkfirst=True)

    # ✅ Step 1: Add the column as nullable
    op.add_column("classes", sa.Column("status", class_status_enum, nullable=True))

    # ✅ Step 2: Fill existing rows with default value
    op.execute("UPDATE classes SET status = 'Active' WHERE status IS NULL")

    # ✅ Step 3: Alter the column to NOT NULL
    op.alter_column("classes", "status", nullable=False)

    # Add the unique constraint on results
    op.create_unique_constraint(
        "uq_result_unique",
        "results",
        ["student_id", "subject_id", "term", "academic_year_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_result_unique", "results", type_="unique")
    op.drop_column("classes", "status")
    class_status_enum.drop(op.get_bind(), checkfirst=True)
