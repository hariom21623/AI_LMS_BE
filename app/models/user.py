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

from app.core.timezone import DEFAULT_TIMEZONE, india_now
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    institute_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("institutes.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    branch_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("branches.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    must_change_password: Mapped[bool] = mapped_column(
    Boolean,
    nullable=False,
    default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default=DEFAULT_TIMEZONE,
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=india_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=india_now,
        onupdate=india_now,
        nullable=False,
    )