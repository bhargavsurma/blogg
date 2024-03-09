"""add content column to posts table

Revision ID: 1fb9bc6a523f
Revises: e467123459d4
Create Date: 2024-02-25 11:36:45.411114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fb9bc6a523f'
down_revision: Union[str, None] = 'e467123459d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
