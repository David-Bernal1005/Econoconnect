"""actualizar_tabla_dato_grafica

Revision ID: c9796668d972
Revises: ca7e65cf99df
Create Date: 2025-11-08 09:24:10.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'c9796668d972'
down_revision = 'ca7e65cf99df'
branch_labels = None
depends_on = None

def upgrade():
    # Añadir nuevas columnas
    with op.batch_alter_table('dato_grafica') as batch_op:
        batch_op.add_column(sa.Column('anio', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cop_usd', sa.DECIMAL(15, 2), nullable=True))
        batch_op.add_column(sa.Column('cop_eur', sa.DECIMAL(15, 2), nullable=True))
        batch_op.add_column(sa.Column('fecha_actualizacion', sa.Date(), nullable=True))

def downgrade():
    # Eliminar columnas añadidas
    with op.batch_alter_table('dato_grafica') as batch_op:
        batch_op.drop_column('fecha_actualizacion')
        batch_op.drop_column('cop_eur')
        batch_op.drop_column('cop_usd')
        batch_op.drop_column('anio')