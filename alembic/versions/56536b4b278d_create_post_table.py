"""create post table

Revision ID: 56536b4b278d
Revises: 
Create Date: 2021-11-04 22:08:53.263751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56536b4b278d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
