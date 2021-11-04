"""add foreign-key to post table

Revision ID: d17f1b3bea24
Revises: 1f688f511184
Create Date: 2021-11-04 22:34:01.183894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd17f1b3bea24'
down_revision = '1f688f511184'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk','posts')
    op.drop_column('posts','owner_id')
    pass
