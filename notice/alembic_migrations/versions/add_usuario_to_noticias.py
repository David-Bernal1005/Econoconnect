"""
Add usuario column to noticias table
Revision ID: add_usuario_to_noticias
Revises: 8e46b434b89b
Create Date: 2025-09-24
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_usuario_to_noticias'
down_revision = '8e46b434b89b'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('noticias', sa.Column('usuario', sa.String(length=100)))

def downgrade():
    op.drop_column('noticias', 'usuario')
