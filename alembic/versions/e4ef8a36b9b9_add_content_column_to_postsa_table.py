"""add content column to postsA table

Revision ID: e4ef8a36b9b9
Revises: 56adb9541a96
Create Date: 2023-09-29 01:33:55.099550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4ef8a36b9b9'
down_revision: Union[str, None] = '56adb9541a96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('postsA', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('postsA', 'content')
