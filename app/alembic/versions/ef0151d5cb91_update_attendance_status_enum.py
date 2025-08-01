"""Update attendance status enum

Revision ID: ef0151d5cb91
Revises: c10e0bf575c6
Create Date: 2025-07-26 08:38:34.071879
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ef0151d5cb91"
down_revision: Union[str, Sequence[str], None] = "c10e0bf575c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

enum_name = "attendancestatusenum"
table_name = "attendances"  # make sure this matches your actual table name
column_name = "status"


def upgrade() -> None:
    conn = op.get_bind()

    # 1. Temporarily change column to TEXT so we can modify values freely
    op.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE TEXT")

    # 2. Update lowercase enum values to title case
    conn.execute(
        sa.text(
            f"UPDATE {table_name} SET {column_name} = 'Present' WHERE {column_name} = 'present'"
        )
    )
    conn.execute(
        sa.text(
            f"UPDATE {table_name} SET {column_name} = 'Absent' WHERE {column_name} = 'absent'"
        )
    )

    # 3. Drop old enum
    op.execute(f"DROP TYPE {enum_name}")

    # 4. Create new enum
    new_enum = sa.Enum("Present", "Absent", "Late", "Excused", name=enum_name)
    new_enum.create(conn)

    # 5. Cast column back to enum type
    op.execute(
        f"ALTER TABLE {table_name} ALTER COLUMN {column_name} "
        f"TYPE {enum_name} USING {column_name}::text::{enum_name}"
    )


def downgrade() -> None:
    conn = op.get_bind()

    # 1. Update values back to lowercase (and fallback for new values)
    conn.execute(
        sa.text(
            f"UPDATE {table_name} SET {column_name} = 'present' WHERE {column_name} = 'Present'"
        )
    )
    conn.execute(
        sa.text(
            f"UPDATE {table_name} SET {column_name} = 'absent' WHERE {column_name} IN ('Absent', 'Late', 'Excused')"
        )
    )

    # 2. Change column type to TEXT temporarily
    op.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE TEXT")

    # 3. Drop updated enum
    op.execute(f"DROP TYPE {enum_name}")

    # 4. Recreate the original enum
    old_enum = sa.Enum("present", "absent", name=enum_name)
    old_enum.create(conn)

    # 5. Re-apply the old enum type to the column
    op.execute(
        f"ALTER TABLE {table_name} ALTER COLUMN {column_name} "
        f"TYPE {enum_name} USING {column_name}::text::{enum_name}"
    )
