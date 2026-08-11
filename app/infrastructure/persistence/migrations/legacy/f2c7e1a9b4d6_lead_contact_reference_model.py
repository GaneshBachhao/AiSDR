"""align Lead with Company + Contact reference model

Revision ID: f2c7e1a9b4d6
Revises: d4a7b1f9c2e3
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "f2c7e1a9b4d6"
down_revision = "d4a7b1f9c2e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "leads" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("leads")}

    if "contact_id" not in columns:
        count = bind.execute(sa.text("SELECT COUNT(*) FROM leads")).scalar_one()
        if count:
            raise RuntimeError(
                "Cannot add required leads.contact_id automatically: "
                "existing Lead rows have no Contact relationship. "
                "Map existing Leads to Contacts before applying this migration."
            )

        with op.batch_alter_table("leads") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "contact_id",
                    sa.UUID(),
                    nullable=True,
                )
            )
            batch_op.create_foreign_key(
                "fk_leads_contact_id_contacts",
                "contacts",
                ["contact_id"],
                ["id"],
                ondelete="RESTRICT",
            )

        columns = {column["name"] for column in sa.inspect(bind).get_columns("leads")}

    null_contacts = bind.execute(
        sa.text("SELECT COUNT(*) FROM leads WHERE contact_id IS NULL")
    ).scalar_one()
    if null_contacts:
        raise RuntimeError(
            "Cannot make leads.contact_id required while existing Lead rows "
            "contain NULL contact_id values."
        )

    with op.batch_alter_table("leads") as batch_op:
        if "source" not in columns:
            batch_op.add_column(
                sa.Column(
                    "source",
                    sa.String(length=50),
                    nullable=True,
                )
            )

        if "score" not in columns:
            batch_op.add_column(
                sa.Column(
                    "score",
                    sa.Integer(),
                    nullable=True,
                )
            )

        if "notes" not in columns:
            batch_op.add_column(
                sa.Column(
                    "notes",
                    sa.String(length=5000),
                    nullable=True,
                )
            )

        if "is_qualified" not in columns:
            batch_op.add_column(
                sa.Column(
                    "is_qualified",
                    sa.Boolean(),
                    nullable=True,
                )
            )

    bind.execute(
        sa.text(
            "UPDATE leads SET source = COALESCE(source, 'Other'), "
            "score = COALESCE(score, 0), "
            "is_qualified = CASE "
            "WHEN UPPER(status) = 'QUALIFIED' THEN TRUE ELSE FALSE END"
        )
    )

    bind.execute(
        sa.text(
            "UPDATE leads SET status = CASE UPPER(status) "
            "WHEN 'NEW' THEN 'New' "
            "WHEN 'CONTACTED' THEN 'Contacted' "
            "WHEN 'QUALIFIED' THEN 'Qualified' "
            "WHEN 'DISQUALIFIED' THEN 'Disqualified' "
            "WHEN 'LOST' THEN 'Disqualified' "
            "WHEN 'CONVERTED' THEN 'Converted' "
            "WHEN 'CLOSED' THEN 'Closed' "
            "ELSE 'New' END"
        )
    )

    with op.batch_alter_table("leads") as batch_op:
        batch_op.alter_column(
            "contact_id",
            existing_type=sa.UUID(),
            nullable=False,
        )
        batch_op.alter_column(
            "source",
            existing_type=sa.String(length=50),
            nullable=False,
            server_default="Other",
        )
        batch_op.alter_column(
            "score",
            existing_type=sa.Integer(),
            nullable=False,
            server_default="0",
        )
        batch_op.alter_column(
            "is_qualified",
            existing_type=sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        )

        for column in ("email", "phone", "website", "contact_name", "job_title"):
            if column in columns:
                batch_op.drop_column(column)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "leads" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("leads")}

    with op.batch_alter_table("leads") as batch_op:
        if "email" not in columns:
            batch_op.add_column(sa.Column("email", sa.String(length=320), nullable=True))
        if "phone" not in columns:
            batch_op.add_column(sa.Column("phone", sa.String(length=50), nullable=True))
        if "website" not in columns:
            batch_op.add_column(sa.Column("website", sa.String(length=500), nullable=True))
        if "contact_name" not in columns:
            batch_op.add_column(sa.Column("contact_name", sa.String(length=200), nullable=True))

        for column in ("source", "score", "notes", "is_qualified"):
            if column in columns:
                batch_op.drop_column(column)
