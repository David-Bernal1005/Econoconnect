"""merge 95eb5ff57d8f and c9796668d972

Revision ID: b3d9c1f3b1ab
Revises: 95eb5ff57d8f, c9796668d972
Create Date: 2025-11-08 09:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b3d9c1f3b1ab'
down_revision = ('95eb5ff57d8f','c9796668d972')
branch_labels = None
depends_on = None

def upgrade():
    # Merge migration: no schema changes required, resolves multiple heads
    pass

def downgrade():
    # No-op downgrade
    pass
