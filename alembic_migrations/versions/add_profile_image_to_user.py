"""
Revision ID: add_profile_image_to_user
Revises: 30e6a759e855
Create Date: 2025-09-28
"""

revision = 'add_profile_image_to_user'
down_revision = '30e6a759e855'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('profile_image', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('users', 'profile_image')
