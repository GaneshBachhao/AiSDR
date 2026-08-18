"""add linkedin_url column to contacts

Revision ID: 9b4c6d1e2f3a
Revises: c1f2d9a8b7e4
Create Date: 2026-08-02 00:00:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "9b4c6d1e2f3a"
down_revision = "c1f2d9a8b7e4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "contacts" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("contacts")}

    if "linkedin_url" not in columns:
        op.add_column(
            "contacts",
            sa.Column("linkedin_url", sa.String(length=500), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "contacts" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("contacts")}

    if "linkedin_url" in columns:
        op.drop_column("contacts", "linkedin_url")
