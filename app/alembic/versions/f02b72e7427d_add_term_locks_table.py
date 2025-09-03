"""add term_locks table

Revision ID: f02b72e7427d
Revises: 4b776c348116
Create Date: 2025-09-03 22:12:29.223217

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f02b72e7427d"
down_revision: Union[str, Sequence[str], None] = "4b776c348116"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
