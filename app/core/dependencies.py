from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


bearer_scheme = HTTPBearer(
    auto_error=True,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the currently authenticated user from JWT access token.
    """

    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise AppException(
            message="Invalid or expired access token.",
            status_code=401,
            code="INVALID_ACCESS_TOKEN",
        )

    subject = payload.get("sub")

    if not subject:
        raise AppException(
            message="Invalid access token.",
            status_code=401,
            code="INVALID_ACCESS_TOKEN",
        )

    try:
        user_id = int(subject)
    except (TypeError, ValueError):
        raise AppException(
            message="Invalid user ID in access token.",
            status_code=401,
            code="INVALID_ACCESS_TOKEN",
        )

    user_repository = UserRepository(db)

    user = user_repository.get_by_id(user_id)

    if not user:
        raise AppException(
            message="User associated with this token was not found.",
            status_code=401,
            code="USER_NOT_FOUND",
        )

    if not user.is_active:
        raise AppException(
            message="User account is inactive.",
            status_code=403,
            code="USER_INACTIVE",
        )

    return user