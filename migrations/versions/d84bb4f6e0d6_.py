"""empty message

Revision ID: d84bb4f6e0d6
Revises: 
Create Date: 2021-06-26 18:26:19.004330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd84bb4f6e0d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_table',
    sa.Column('sno', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('emailid', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('sno'),
    sa.UniqueConstraint('sno')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_table')
    # ### end Alembic commands ###
