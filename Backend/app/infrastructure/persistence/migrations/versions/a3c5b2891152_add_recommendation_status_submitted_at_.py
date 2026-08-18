"""add recommendation status/submitted_at/approved_at columns

Revision ID: a3c5b2891152
Revises: d7119ce9b04a
Create Date: 2026-08-18 14:50:32.367538

"""

from alembic import op
import sqlalchemy as sa



revision = 'a3c5b2891152'
down_revision = 'd7119ce9b04a'
branch_labels = None
depends_on = None


def upgrade():
    # Existing rows have no value for the new NOT NULL `status` column --
    # a server_default is required so SQLite can backfill them (every
    # pre-existing Recommendation really was created as Draft, since
    # Submit/Approve were never reachable before this).
    op.add_column(
        'recommendations',
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Draft'),
    )
    op.add_column('recommendations', sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('recommendations', sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    op.drop_column('recommendations', 'approved_at')
    op.drop_column('recommendations', 'submitted_at')
    op.drop_column('recommendations', 'status')