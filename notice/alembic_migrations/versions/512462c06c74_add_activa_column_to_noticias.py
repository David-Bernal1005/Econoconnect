"""
Revision ID: 512462c06c74
Revises: add_usuario_to_noticias
Create Date: 2025-09-24 10:37:29.736186

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '512462c06c74'
down_revision = 'add_usuario_to_noticias'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('noticias', sa.Column('activa', sa.Boolean(), nullable=False, server_default=sa.text('1')))
    # ### end Alembic commands ###

def downgrade():
    op.drop_column('noticias', 'activa')
    # ### end Alembic commands ###