"""Rename attendances to attendance

Revision ID: 2ed66a90fd8a
Revises: 73a0d811ad73
Create Date: 2025-08-01 21:59:47.759174

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ed66a90fd8a"
down_revision: Union[str, Sequence[str], None] = "73a0d811ad73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
