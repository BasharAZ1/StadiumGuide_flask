"""Initial migration

Revision ID: 87ab59b0c326
Revises: cf382336bb71
Create Date: 2024-01-29 23:31:38.428811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87ab59b0c326'
down_revision = 'cf382336bb71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stadium')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('stadium',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('stadium_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('location', sa.VARCHAR(length=100), nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), nullable=True),
    sa.Column('capacity', sa.INTEGER(), nullable=True),
    sa.Column('owner', sa.VARCHAR(length=50), nullable=True),
    sa.Column('yearBuilt', sa.INTEGER(), nullable=True),
    sa.Column('fieldSize', sa.VARCHAR(length=50), nullable=True),
    sa.Column('stadiumImage', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
