"""align leads table with current contract

Revision ID: d4a7b1f9c2e3
Revises: 9b4c6d1e2f3a
Create Date: 2026-08-02 00:00:00.000000

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "d4a7b1f9c2e3"
down_revision = "9b4c6d1e2f3a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "leads" not in inspector.get_table_names():
        return

    with op.batch_alter_table("leads") as batch_op:
        existing_columns = {column["name"] for column in inspector.get_columns("leads")}

        if "contact_name" in existing_columns:
            batch_op.drop_column("contact_name")

        if "job_title" in existing_columns:
            batch_op.drop_column("job_title")

        if "contact_id" not in existing_columns:
            batch_op.add_column(
                sa.Column(
                    "contact_id",
                    sa.UUID(),
                    sa.ForeignKey("contacts.id", ondelete="RESTRICT"),
                    nullable=True,
                )
            )

        if "website" not in existing_columns:
            batch_op.add_column(
                sa.Column("website", sa.String(length=500), nullable=True)
            )

        if "status" not in existing_columns:
            batch_op.add_column(
                sa.Column(
                    "status",
                    sa.String(length=50),
                    nullable=False,
                    server_default=sa.text("'NEW'"),
                )
            )

    remaining_columns = {column["name"] for column in sa.inspect(bind).get_columns("leads")}

    if "ix_leads_company_id" not in {index["name"] for index in inspector.get_indexes("leads")}:
        op.create_index("ix_leads_company_id", "leads", ["company_id"], unique=False)

    if "ix_leads_email" not in {index["name"] for index in inspector.get_indexes("leads")}:
        op.create_index("ix_leads_email", "leads", ["email"], unique=False)

    if "ix_leads_contact_id" not in {index["name"] for index in inspector.get_indexes("leads")} and "contact_id" in remaining_columns:
        op.create_index("ix_leads_contact_id", "leads", ["contact_id"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "leads" not in inspector.get_table_names():
        return

    with op.batch_alter_table("leads") as batch_op:
        existing_columns = {column["name"] for column in inspector.get_columns("leads")}

        if "status" in existing_columns:
            batch_op.drop_column("status")

        if "website" in existing_columns:
            batch_op.drop_column("website")

        if "contact_id" in existing_columns:
            batch_op.drop_column("contact_id")

        if "contact_name" not in existing_columns:
            batch_op.add_column(
                sa.Column("contact_name", sa.String(length=200), nullable=False)
            )

        if "job_title" not in existing_columns:
            batch_op.add_column(
                sa.Column("job_title", sa.String(length=150), nullable=True)
            )

    indexes = {index["name"] for index in inspector.get_indexes("leads")}

    if "ix_leads_contact_id" in indexes:
        op.drop_index("ix_leads_contact_id", table_name="leads")

    if "ix_leads_email" in indexes:
        op.drop_index("ix_leads_email", table_name="leads")

    if "ix_leads_company_id" in indexes:
        op.drop_index("ix_leads_company_id", table_name="leads")
