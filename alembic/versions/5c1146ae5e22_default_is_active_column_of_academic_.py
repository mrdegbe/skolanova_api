"""Default is_active column of academic_years to false

Revision ID: 5c1146ae5e22
Revises: 64977c107f36
Create Date: 2025-07-22 19:45:40.543146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c1146ae5e22'
down_revision: Union[str, Sequence[str], None] = '64977c107f36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        "unique_active_academic_year",
        "academic_years",
        ["is_active"],
        unique=True,
        postgresql_where=sa.text("is_active = TRUE")
    )

def downgrade():
    op.drop_index("unique_active_academic_year", table_name="academic_years")