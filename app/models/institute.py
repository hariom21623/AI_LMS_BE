from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.timezone import DEFAULT_TIMEZONE, india_now
from app.db.database import Base


class Institute(Base):
    __tablename__ = "institutes"

    # ========================================================
    # PRIMARY KEY
    # ========================================================

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    # ========================================================
    # CONTACT INFORMATION
    # ========================================================

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========================================================
    # BRANDING
    # ========================================================

    logo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ========================================================
    # COUNTRY & TIMEZONE
    # ========================================================

    country_code: Mapped[str] = mapped_column(
        String(2),
        default="IN",
        nullable=False,
        index=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default=DEFAULT_TIMEZONE,
        nullable=False,
    )

    # ========================================================
    # STATUS
    # ========================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

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