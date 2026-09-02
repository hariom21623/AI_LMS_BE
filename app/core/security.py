from datetime import datetime, timedelta, timezone
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)
from jose import JWTError, jwt

from app.core.config import settings


password_hasher = PasswordHasher()


# =========================================================
# Password Hashing
# =========================================================

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2id.
    """
    return password_hasher.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Verify a plain-text password against an Argon2 password hash.
    """
    try:
        return password_hasher.verify(
            password_hash,
            password,
        )
    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError,
    ):
        return False


# =========================================================
# JWT
# =========================================================

def create_access_token(
    subject: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a short-lived access token.
    """

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": expire,
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm="HS256",
    )


def create_refresh_token(
    subject: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a long-lived refresh token.
    """

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "iat": now,
        "exp": expire,
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET,
        algorithm="HS256",
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decode and validate an access token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )

        if payload.get("type") != "access":
            return None

        if not payload.get("sub"):
            return None

        return payload

    except JWTError:
        return None


def decode_refresh_token(token: str) -> dict[str, Any] | None:
    """
    Decode and validate a refresh token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET,
            algorithms=["HS256"],
        )

        if payload.get("type") != "refresh":
            return None

        if not payload.get("sub"):
            return None

        return payload

    except JWTError:
        return None