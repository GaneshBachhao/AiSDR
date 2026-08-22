"""add missing recommendation solutions column

Revision ID: 107b2a2f4791
Revises: 96d650220052
Create Date: 2026-08-22 19:00:04.515783

RecommendationModel.solutions has existed on the ORM model since the
Recommendation aggregate was built, but no migration was ever generated for
it -- every database built from the migration chain alone (rather than
Base.metadata.create_all) has been missing this column, causing every
GET /recommendations call to fail with `sqlite3.OperationalError: no such
column: recommendations.solutions`. Autogenerate also flagged
`leads.review_status`/`recommendations.status` server_default drops -- both
are the same known false-positive drift already stripped from the EPIC-09.2
migration (SQLite server_default representation differences, not real
changes), so this migration only carries the one real fix.
"""

import sqlalchemy as sa
from alembic import op

revision = "107b2a2f4791"
down_revision = "96d650220052"
branch_labels = None
depends_on = None


def upgrade():
    # Existing rows have no value for the new NOT NULL `solutions` column --
    # a server_default is required so SQLite can backfill them, same pattern
    # as a3c5b2891152's `status` column.
    op.add_column(
        "recommendations",
        sa.Column("solutions", sa.Text(), nullable=False, server_default="[]"),
    )


def downgrade():
    op.drop_column("recommendations", "solutions")
