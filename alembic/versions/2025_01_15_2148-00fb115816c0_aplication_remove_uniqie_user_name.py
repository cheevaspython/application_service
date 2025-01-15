"""aplication remove uniqie -> user_name

Revision ID: 00fb115816c0
Revises: 8c3dc05b2077
Create Date: 2025-01-15 21:48:48.269976

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "00fb115816c0"
down_revision: Union[str, None] = "8c3dc05b2077"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_applications_user_name", "applications", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint(
        "uq_applications_user_name", "applications", ["user_name"]
    )
