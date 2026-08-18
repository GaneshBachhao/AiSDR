"""create contacts table with company reference

Revision ID: c1f2d9a8b7e4
Revises: 7e5b22b5d8a1
Create Date: 2026-07-28 00:00:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "c1f2d9a8b7e4"
down_revision = "7e5b22b5d8a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "contacts" not in inspector.get_table_names():
        op.create_table(
            "contacts",
            sa.Column("id", sa.UUID(), nullable=False),
            sa.Column("first_name", sa.String(length=100), nullable=False),
            sa.Column("last_name", sa.String(length=100), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("phone", sa.String(length=50), nullable=True),
            sa.Column("job_title", sa.String(length=150), nullable=True),
            sa.Column("company_id", sa.UUID(), nullable=False),
            sa.Column("company_name", sa.String(length=255), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["company_id"],
                ["companies.id"],
                name=op.f("fk_contacts_company_id_companies"),
                ondelete="RESTRICT",
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_contacts")),
        )
        op.create_index(op.f("ix_contacts_email"), "contacts", ["email"], unique=True)
        op.create_index(op.f("ix_contacts_company_id"), "contacts", ["company_id"], unique=False)
        return

    columns = {column["name"] for column in inspector.get_columns("contacts")}

    if "company_id" not in columns:
        op.add_column(
            "contacts",
            sa.Column("company_id", sa.UUID(), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "contacts" in inspector.get_table_names():
        indexes = {index["name"] for index in inspector.get_indexes("contacts")}

        if op.f("ix_contacts_company_id") in indexes:
            op.drop_index(op.f("ix_contacts_company_id"), table_name="contacts")

        if op.f("ix_contacts_email") in indexes:
            op.drop_index(op.f("ix_contacts_email"), table_name="contacts")

        op.drop_table("contacts")
