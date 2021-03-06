"""empty message

Revision ID: 0892385972ba
Revises: 
Create Date: 2020-03-01 18:20:45.310043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0892385972ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('cryptotext', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    # ### end Alembic commands ###
