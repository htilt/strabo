"""test column

Revision ID: 2e3759e9a425
Revises: 
Create Date: 2016-06-23 22:56:25.494389

"""

# revision identifiers, used by Alembic.
revision = '2e3759e9a425'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
    	'test',
    	sa.Column('id',sa.Integer,primary_key=True),
    )

def downgrade():
    op.drop_table('test')
