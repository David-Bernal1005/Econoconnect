"""add etiquetas column to noticias

Revision ID: add_etiquetas_to_noticias
Revises: 
Create Date: 2025-10-01
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'add_etiquetas_to_noticias'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('noticias', sa.Column('etiquetas', sa.String(length=1000), nullable=True))

def downgrade():
    op.drop_column('noticias', 'etiquetas')
