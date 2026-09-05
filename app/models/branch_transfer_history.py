from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Identity,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import india_now
from app.db.database import Base


class BranchTransferHistory(Base):
    __tablename__ = "branch_transfer_history"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    branch_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "branches.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    from_institute_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "institutes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    to_institute_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "institutes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    transferred_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    transferred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=india_now,
        nullable=False,
    )

    is_reversed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    reversed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reversed_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )