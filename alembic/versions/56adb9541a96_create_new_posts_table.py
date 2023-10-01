"""create new posts table

Revision ID: 56adb9541a96
Revises: 
Create Date: 2023-09-28 23:46:41.907640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56adb9541a96'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('postsA', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                   sa.Column('title', sa.String(), nullable=False))
    


def downgrade() -> None:
    op.drop_table('postsA')
