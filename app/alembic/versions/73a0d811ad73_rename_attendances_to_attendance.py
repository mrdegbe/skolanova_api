"""Rename attendances to attendance

Revision ID: 73a0d811ad73
Revises: ef0151d5cb91
Create Date: 2025-08-01 21:56:49.160402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73a0d811ad73'
down_revision: Union[str, Sequence[str], None] = 'ef0151d5cb91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
