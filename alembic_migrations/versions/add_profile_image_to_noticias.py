"""
Revision ID: add_profile_image_to_noticias
Revises: None
Create Date: 2025-10-01
"""

revision = 'add_profile_image_to_noticias'
down_revision = '6890aeac7c6f'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('noticias', sa.Column('profile_image', sa.String(length=1000000), nullable=True))

def downgrade():
    op.drop_column('noticias', 'profile_image')
