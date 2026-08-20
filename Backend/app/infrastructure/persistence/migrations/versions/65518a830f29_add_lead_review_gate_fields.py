"""add lead review gate fields

Revision ID: 65518a830f29
Revises: a3c5b2891152
Create Date: 2026-08-19 15:54:43.143965

"""

from alembic import op
import sqlalchemy as sa



revision = '65518a830f29'
down_revision = 'a3c5b2891152'
branch_labels = None
depends_on = None


def upgrade():
    # server_default backfills existing rows to "Not Submitted" -- matches
    # every prior status-column addition in this project (e.g. the
    # Recommendation status column, a3c5b2891152).
    op.add_column(
        'leads',
        sa.Column(
            'review_status',
            sa.String(length=50),
            nullable=False,
            server_default='Not Submitted',
        ),
    )
    op.add_column('leads', sa.Column('review_submitted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('leads', sa.Column('review_decided_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('leads', sa.Column('review_notes', sa.String(length=2000), nullable=True))


def downgrade():
    op.drop_column('leads', 'review_notes')
    op.drop_column('leads', 'review_decided_at')
    op.drop_column('leads', 'review_submitted_at')
    op.drop_column('leads', 'review_status')