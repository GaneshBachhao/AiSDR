"""add suppression entries table

Revision ID: d532a1622ed8
Revises: 65518a830f29
Create Date: 2026-08-19 18:19:35.549825

"""

from alembic import op
import sqlalchemy as sa



revision = 'd532a1622ed8'
down_revision = '65518a830f29'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'suppression_entries',
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('reason', sa.String(length=50), nullable=False),
        sa.Column('notes', sa.String(length=2000), nullable=True),
        sa.Column('suppressed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column('created_by', sa.String(length=100), nullable=True),
        sa.Column('updated_by', sa.String(length=100), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_suppression_entries')),
    )
    op.create_index(op.f('ix_suppression_entries_email'), 'suppression_entries', ['email'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_suppression_entries_email'), table_name='suppression_entries')
    op.drop_table('suppression_entries')