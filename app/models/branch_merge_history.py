from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import india_now
from app.db.database import Base


class BranchMergeHistory(Base):
    __tablename__ = "branch_merge_history"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    source_branch_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "branches.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    target_branch_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "branches.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    source_institute_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "institutes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    target_institute_id: Mapped[int | None] = mapped_column(
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

    merged_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    merged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=india_now,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="COMPLETED",
        nullable=False,
        index=True,
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