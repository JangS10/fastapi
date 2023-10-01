"""add foreogn-key to posts table

Revision ID: 638a77c1ec2f
Revises: 98d505d0da8a
Create Date: 2023-09-29 01:49:58.995759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '638a77c1ec2f'
down_revision: Union[str, None] = '98d505d0da8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('postsA', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('postA_users_fk', source_table="postsA", referent_table="usersA",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    


def downgrade() -> None:
    op.drop_constraint('postA_users_fk', table_name="postsA")
    op.drop_column('postsA', 'owner_id')
