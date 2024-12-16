"""add start_date and end_date to tasks

Revision ID: b79fc4d23421
Revises: 
Create Date: 2024-12-14 13:17:00.488968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b79fc4d23421'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('start_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('end_date', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('tasks', 'start_date')
    op.drop_column('tasks', 'end_date')