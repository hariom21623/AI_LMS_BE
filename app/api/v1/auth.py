from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new unassigned user.
    """

    service = AuthService(db)

    user = service.register_user(data)

    return user


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login using email and password.
    """

    service = AuthService(db)

    user = service.authenticate_user(
        email=data.email,
        password=data.password,
    )

    # Update last login time
    user.last_login_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)

    # Create access token
    access_token = create_access_token(
        subject=str(user.id),
        extra_claims={
            "institute_id": (
                user.institute_id
                if user.institute_id is not None
                else None
            ),
            "branch_id": (
                user.branch_id
                if user.branch_id is not None
                else None
            ),
        },
    )

    # Create refresh token
    refresh_token = create_refresh_token(
        subject=str(user.id),
    )

    return LoginResponse(
        user=user,
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )
    
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get currently authenticated user.
    """

    return current_user