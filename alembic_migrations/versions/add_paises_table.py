"""Agregar tabla paises y relación con usuarios

Revision ID: add_paises_table
Revises: 
Create Date: 2025-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_paises_table'
down_revision = '9461cff7e7f7'  # Cambiar por la última migración
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla paises
    op.create_table('paises',
        sa.Column('id_pais', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('codigo_iso', sa.String(length=3), nullable=True),
        sa.Column('codigo_telefono', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('id_pais'),
        sa.UniqueConstraint('codigo_iso'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_paises_id_pais'), 'paises', ['id_pais'], unique=False)
    
    # Agregar columna id_pais a la tabla users
    op.add_column('users', sa.Column('id_pais', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'paises', ['id_pais'], ['id_pais'])
    
    # Insertar algunos países de ejemplo
    op.execute("""
        INSERT INTO paises (nombre, codigo_iso, codigo_telefono) VALUES
        ('Colombia', 'COL', '+57'),
        ('Estados Unidos', 'USA', '+1'),
        ('México', 'MEX', '+52'),
        ('Argentina', 'ARG', '+54'),
        ('Brasil', 'BRA', '+55'),
        ('Chile', 'CHL', '+56'),
        ('Perú', 'PER', '+51'),
        ('Ecuador', 'ECU', '+593'),
        ('Venezuela', 'VEN', '+58'),
        ('España', 'ESP', '+34'),
        ('Francia', 'FRA', '+33'),
        ('Reino Unido', 'GBR', '+44'),
        ('Alemania', 'DEU', '+49'),
        ('Italia', 'ITA', '+39'),
        ('Canadá', 'CAN', '+1'),
        ('Australia', 'AUS', '+61'),
        ('Japón', 'JPN', '+81'),
        ('China', 'CHN', '+86'),
        ('India', 'IND', '+91'),
        ('Rusia', 'RUS', '+7')
    """)

def downgrade():
    # Eliminar foreign key y columna id_pais de users
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'id_pais')
    
    # Eliminar tabla paises
    op.drop_index(op.f('ix_paises_id_pais'), table_name='paises')
    op.drop_table('paises')