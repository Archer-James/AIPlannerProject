"""empty message

Revision ID: 9e5784e99907
Revises: 42ef1f4ae570, b7a426eb324c
Create Date: 2024-10-21 12:37:52.355211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e5784e99907'
down_revision: Union[str, None] = ('42ef1f4ae570', 'b7a426eb324c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
