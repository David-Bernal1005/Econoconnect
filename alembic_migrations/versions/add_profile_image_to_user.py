"""
Revision ID: add_profile_image_to_user
Revises: None
Create Date: 2025-09-28
"""

revision = 'add_profile_image_to_user'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('profile_image', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('users', 'profile_image')
"""
Revision ID: add_profile_image_to_user
Revises: None
Create Date: 2025-09-28
"""

revision = 'add_profile_image_to_user'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('profile_image', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('users', 'profile_image')
