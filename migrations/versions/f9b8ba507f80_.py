"""empty message

Revision ID: f9b8ba507f80
Revises: 89a9e557f787
Create Date: 2020-05-16 14:33:11.370550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9b8ba507f80'
down_revision = '89a9e557f787'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(length=4294000000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quote', sa.String(length=4294000000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quotes')
    op.drop_table('notes')
    # ### end Alembic commands ###
