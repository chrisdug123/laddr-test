"""empty message

Revision ID: 3d94922d1216
Revises: f88fb0124048
Create Date: 2024-08-20 08:27:37.910414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d94922d1216'
down_revision = 'f88fb0124048'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'locations', ['location_id'], ['id'])
        batch_op.drop_column('locations')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('locations', sa.VARCHAR(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'locations', ['locations'], ['location_name'])
        batch_op.drop_column('location_id')

    # ### end Alembic commands ###
