"""old fix

Revision ID: 6e21e4c342f5
Revises: 645cb6297910
Create Date: 2022-10-18 11:27:23.306887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e21e4c342f5'
down_revision = '645cb6297910'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trs398_electrons', schema=None) as batch_op:
        batch_op.drop_column('pdd_data_e')
        batch_op.drop_column('temp_press_e')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trs398_electrons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('temp_press_e', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('pdd_data_e', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
