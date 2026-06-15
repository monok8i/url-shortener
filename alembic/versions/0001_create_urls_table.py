"""Create urls table.

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the urls table and the short_code index."""
    op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "short_code",
            sa.String(length=10),
            nullable=False,
        ),
        sa.Column(
            "original_url",
            sa.String(length=2048),
            nullable=False,
        ),
        sa.Column(
            "clicks",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_urls_short_code", "urls", ["short_code"], unique=True)


def downgrade() -> None:
    """Drop the urls table and the short_code index."""
    op.drop_index("ix_urls_short_code", table_name="urls")
    op.drop_table("urls")
