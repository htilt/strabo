"""add column to table

Revision ID: a650cd84422a
Revises: 2e3759e9a425
Create Date: 2016-06-23 22:58:52.353107

"""

# revision identifiers, used by Alembic.
revision = 'a650cd84422a'
down_revision = '2e3759e9a425'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('test',sa.Column('new column',sa.Integer))


def downgrade():
    op.drop_column('test','new column')
