from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.database import get_db
from app.models.branch import Branch
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


def _get_user_role_codes(
    db: Session,
    user_id: int,
) -> set[str]:
    """
    Get all active role codes assigned to a user.
    """

    stmt = (
        select(Role.code)
        .join(
            UserRole,
            UserRole.role_id == Role.id,
        )
        .where(
            UserRole.user_id == user_id,
            Role.is_active.is_(True),
        )
    )

    return set(
        db.scalars(stmt).all()
    )


def _is_super_admin(
    db: Session,
    user: User,
) -> bool:
    """
    Check whether the user has a global
    SUPER_ADMIN role.
    """

    role_codes = _get_user_role_codes(
        db=db,
        user_id=user.id,
    )

    return "SUPER_ADMIN" in role_codes


def require_branch_create_access(
    institute_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate whether the current user can create
    a branch under the requested institute.

    Super Admin:
        Can create under any institute.

    Institute Admin:
        Can create only under own institute.

    Other users:
        Access denied.
    """

    if _is_super_admin(
        db=db,
        user=current_user,
    ):
        return current_user

    if (
        current_user.institute_id is None
        or current_user.institute_id != institute_id
    ):
        raise AppException(
            message="You do not have access to this institute.",
            status_code=403,
            code="INSTITUTE_ACCESS_DENIED",
        )

    return current_user


def require_branch_access(
    branch_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate whether the current user can access
    the requested branch.

    Super Admin:
        Can access any branch.

    Institute users:
        Can access branches belonging to their institute.

    Branch Admin:
        Must additionally belong to the requested branch.
    """

    branch = db.scalar(
        select(Branch).where(
            Branch.id == branch_id
        )
    )

    if not branch:
        raise AppException(
            message="Branch not found.",
            status_code=404,
            code="BRANCH_NOT_FOUND",
        )

    if _is_super_admin(
        db=db,
        user=current_user,
    ):
        return current_user

    if (
        current_user.institute_id is None
        or current_user.institute_id != branch.institute_id
    ):
        raise AppException(
            message="You do not have access to this branch.",
            status_code=403,
            code="BRANCH_ACCESS_DENIED",
        )

    # If the user is assigned to a specific branch,
    # they can access only that branch.
    if (
        current_user.branch_id is not None
        and current_user.branch_id != branch.id
    ):
        raise AppException(
            message="You do not have access to this branch.",
            status_code=403,
            code="BRANCH_ACCESS_DENIED",
        )

    return current_user


def require_institute_branch_read_access(
    institute_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate access to all branches of an institute.

    Super Admin:
        Can read branches of any institute.

    Institute users:
        Can read branches only from their own institute.

    Branch-level users:
        Can read only their own assigned branch through
        their institute.
    """

    if _is_super_admin(
        db=db,
        user=current_user,
    ):
        return current_user

    if (
        current_user.institute_id is None
        or current_user.institute_id != institute_id
    ):
        raise AppException(
            message="You do not have access to this institute.",
            status_code=403,
            code="INSTITUTE_ACCESS_DENIED",
        )

    return current_user