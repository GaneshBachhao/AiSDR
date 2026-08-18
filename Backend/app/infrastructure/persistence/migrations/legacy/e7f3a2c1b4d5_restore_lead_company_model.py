"""Restore Lead to the Company/Account business model.

Revision ID: e7f3a2c1b4d5
Revises: d4a7b1f9c2e3
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "e7f3a2c1b4d5"
down_revision = "d4a7b1f9c2e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "leads" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("leads")}

    # Restore contact_name as application/domain data.
    if "contact_name" not in columns:
        with op.batch_alter_table("leads") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "contact_name",
                    sa.String(length=200),
                    nullable=True,
                )
            )

    columns = {column["name"] for column in sa.inspect(bind).get_columns("leads")}

    # If the previous schema has contact_id, use the related Contact name
    # as the Lead's stored contact snapshot before removing the relationship.
    if "contact_id" in columns and "contact_name" in columns:
        bind.execute(
            sa.text(
                """
                UPDATE leads
                SET contact_name = (
                    SELECT TRIM(
                        COALESCE(c.first_name, '') ||
                        CASE
                            WHEN c.last_name IS NOT NULL
                                 AND c.last_name <> ''
                            THEN ' ' || c.last_name
                            ELSE ''
                        END
                    )
                    FROM contacts c
                    WHERE c.id = leads.contact_id
                )
                WHERE contact_name IS NULL
                  AND contact_id IS NOT NULL
                """
            )
        )

    # Existing rows that cannot be mapped from a Contact must be resolved
    # explicitly rather than silently inventing a business identity.
    missing = bind.execute(
        sa.text("SELECT COUNT(*) FROM leads WHERE contact_name IS NULL OR TRIM(contact_name) = ''")
    ).scalar_one()

    if missing:
        raise RuntimeError(
            "Lead migration cannot complete: existing Lead rows have no "
            "contact_name. Resolve those rows before applying this migration."
        )

    with op.batch_alter_table("leads") as batch_op:
        if "contact_id" in columns:
            batch_op.drop_column("contact_id")

        if "website" in columns:
            batch_op.drop_column("website")

        if "job_title" in columns:
            batch_op.drop_column("job_title")

    # Normalize legacy enum names to the current enum values.
    bind.execute(
        sa.text(
            "UPDATE leads SET status = "
            "CASE UPPER(status) "
            "WHEN 'NEW' THEN 'New' "
            "WHEN 'CONTACTED' THEN 'Contacted' "
            "WHEN 'QUALIFIED' THEN 'Qualified' "
            "WHEN 'DISQUALIFIED' THEN 'Disqualified' "
            "WHEN 'CONVERTED' THEN 'Converted' "
            "WHEN 'CLOSED' THEN 'Closed' "
            "ELSE status END"
        )
    )

    bind.execute(
        sa.text(
            "UPDATE leads SET source = "
            "CASE UPPER(source) "
            "WHEN 'WEBSITE' THEN 'Website' "
            "WHEN 'REFERRAL' THEN 'Referral' "
            "WHEN 'LINKEDIN' THEN 'LinkedIn' "
            "WHEN 'EMAIL' THEN 'Email' "
            "WHEN 'PHONE' THEN 'Phone' "
            "WHEN 'EVENT' THEN 'Event' "
            "WHEN 'PARTNER' THEN 'Partner' "
            "WHEN 'OTHER' THEN 'Other' "
            "ELSE source END"
        )
    )

    # contact_name is now a required Lead invariant.
    with op.batch_alter_table("leads") as batch_op:
        batch_op.alter_column(
            "contact_name",
            existing_type=sa.String(length=200),
            nullable=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "leads" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("leads")}

    with op.batch_alter_table("leads") as batch_op:
        if "website" not in columns:
            batch_op.add_column(
                sa.Column(
                    "website",
                    sa.String(length=500),
                    nullable=True,
                )
            )

        if "contact_id" not in columns:
            batch_op.add_column(
                sa.Column(
                    "contact_id",
                    sa.UUID(),
                    nullable=True,
                )
            )

        if "job_title" not in columns:
            batch_op.add_column(
                sa.Column(
                    "job_title",
                    sa.String(length=150),
                    nullable=True,
                )
            )
