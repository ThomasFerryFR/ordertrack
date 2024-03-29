"""order table

Revision ID: 364bcebb2639
Revises: af987c9246c1
Create Date: 2018-04-22 16:14:51.741094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '364bcebb2639'
down_revision = 'af987c9246c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('tracker_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'tracker', ['tracker_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'tracker_id')
    # ### end Alembic commands ###
