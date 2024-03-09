"""create posts table

Revision ID: e467123459d4
Revises: 
Create Date: 2024-02-25 11:29:32.967789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e467123459d4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable = False, primary_key= True)
                    ,sa.Column('title',sa.String(),nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
