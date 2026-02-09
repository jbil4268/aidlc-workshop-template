"""add table capacity

Revision ID: 002
Revises: 001
Create Date: 2026-02-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add capacity column to tables
    op.add_column('tables', sa.Column('capacity', sa.Integer(), nullable=False, server_default='4'))


def downgrade():
    # Remove capacity column from tables
    op.drop_column('tables', 'capacity')
