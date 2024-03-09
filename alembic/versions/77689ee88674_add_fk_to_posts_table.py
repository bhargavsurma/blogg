"""add FK to posts table

Revision ID: 77689ee88674
Revises: 731bdcf95c7f
Create Date: 2024-02-25 18:01:17.377358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77689ee88674'
down_revision: Union[str, None] = '731bdcf95c7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('FK_posts_owner_id',source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'],ondelete="cascade")
    pass


def downgrade() -> None:
    op.drop_constraint('FK_posts_owner_id',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
