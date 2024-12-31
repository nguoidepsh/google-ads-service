"""Add uuid request

Revision ID: 419f90e1a0dc
Revises: a273949a690e
Create Date: 2024-12-29 03:54:50.134511

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "419f90e1a0dc"
down_revision: Union[str, None] = "a273949a690e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("Requests", sa.Column("uuid", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Requests", "uuid")
    # ### end Alembic commands ###
