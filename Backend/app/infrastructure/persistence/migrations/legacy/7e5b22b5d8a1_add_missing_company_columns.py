"""add missing company columns

Revision ID: 7e5b22b5d8a1
Revises: 23e07b7dfb24
Create Date: 2026-07-28 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "7e5b22b5d8a1"
down_revision = "23e07b7dfb24"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "companies",
        sa.Column("company_size", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("country", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("state", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("city", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    op.drop_column("companies", "is_active")
    op.drop_column("companies", "city")
    op.drop_column("companies", "state")
    op.drop_column("companies", "country")
    op.drop_column("companies", "company_size")
