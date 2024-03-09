"""add user table

Revision ID: 731bdcf95c7f
Revises: 1fb9bc6a523f
Create Date: 2024-02-25 16:36:26.388976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '731bdcf95c7f'
down_revision: Union[str, None] = '1fb9bc6a523f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('Now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                                )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
