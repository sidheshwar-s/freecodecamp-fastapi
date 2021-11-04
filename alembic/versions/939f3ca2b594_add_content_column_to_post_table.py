"""add content column to post table

Revision ID: 939f3ca2b594
Revises: 56536b4b278d
Create Date: 2021-11-04 22:21:46.942657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '939f3ca2b594'
down_revision = '56536b4b278d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
