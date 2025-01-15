"""aplication

Revision ID: 8c3dc05b2077
Revises: 
Create Date: 2025-01-15 13:38:13.183429

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8c3dc05b2077"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "applications",
        sa.Column("user_name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column(
            "created_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('Europe/Moscow', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('Europe/Moscow', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_applications")),
        sa.UniqueConstraint("user_name", name=op.f("uq_applications_user_name")),
    )


def downgrade() -> None:
    op.drop_table("applications")
