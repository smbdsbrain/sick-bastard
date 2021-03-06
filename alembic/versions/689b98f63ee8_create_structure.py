"""Create structure

Revision ID: 689b98f63ee8
Revises: 
Create Date: 2018-07-29 02:57:48.324721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689b98f63ee8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('begins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ends',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vertexes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vertexes')
    op.drop_table('ends')
    op.drop_table('edges')
    op.drop_table('begins')
    # ### end Alembic commands ###
