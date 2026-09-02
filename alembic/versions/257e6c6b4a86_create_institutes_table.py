"""create institutes table

Revision ID: 257e6c6b4a86
Revises:
Create Date: 2026-09-02 12:29:03.753711
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "257e6c6b4a86"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create institutes table."""

    op.create_table(
        "institutes",

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
        ),

        sa.Column(
            "code",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "email",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=True,
        ),

        sa.Column(
            "address",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "logo_url",
            sa.String(length=500),
            nullable=True,
        ),

        sa.Column(
            "country_code",
            sa.String(length=2),
            nullable=False,
        ),

        sa.Column(
            "timezone",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_index(
        "ix_institutes_code",
        "institutes",
        ["code"],
        unique=True,
    )

    op.create_index(
        "ix_institutes_country_code",
        "institutes",
        ["country_code"],
        unique=False,
    )


def downgrade() -> None:
    """Drop institutes table."""

    op.drop_index(
        "ix_institutes_country_code",
        table_name="institutes",
    )

    op.drop_index(
        "ix_institutes_code",
        table_name="institutes",
    )

    op.drop_table("institutes")