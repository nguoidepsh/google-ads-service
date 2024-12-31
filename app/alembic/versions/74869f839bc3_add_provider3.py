"""Add provider3

Revision ID: 74869f839bc3
Revises: 718afcc0a9ee
Create Date: 2024-12-28 15:48:08.290307

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "74869f839bc3"
down_revision: Union[str, None] = "718afcc0a9ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum("PROMO", "INVOICE", "DISCOUNT", name="providertype").create(op.get_bind())
    op.add_column(
        "Providers",
        sa.Column(
            "type",
            postgresql.ENUM(
                "PROMO", "INVOICE", "DISCOUNT", name="providertype", create_type=False
            ),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Providers", "type")
    sa.Enum("PROMO", "INVOICE", "DISCOUNT", name="providertype").drop(op.get_bind())
    # ### end Alembic commands ###
