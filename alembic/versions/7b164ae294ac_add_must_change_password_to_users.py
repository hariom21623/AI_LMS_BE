"""add must change password to users

Revision ID: 7b164ae294ac
Revises: 64f665a9e697
Create Date: 2026-09-02
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b164ae294ac"
down_revision: Union[str, Sequence[str], None] = "64f665a9e697"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add must_change_password to users.

    Existing users receive False.
    """

    op.add_column(
        "users",
        sa.Column(
            "must_change_password",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    # Remove database-level default after existing
    # rows have been populated.
    op.alter_column(
        "users",
        "must_change_password",
        server_default=None,
    )


def downgrade() -> None:
    """
    Remove must_change_password from users.
    """

    op.drop_column(
        "users",
        "must_change_password",
    )