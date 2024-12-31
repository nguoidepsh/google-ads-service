"""add tables to example_schema

Revision ID: 1a512ea12808
Revises: 3d3469184945
Create Date: 2024-12-22 02:45:59.647953

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1a512ea12808"
down_revision: Union[str, None] = "3d3469184945"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Accounts",
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.add_column(
        "Accounts",
        sa.Column(
            "login_customer_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Accounts", "login_customer_id")
    op.drop_column("Accounts", "email")
    # ### end Alembic commands ###
