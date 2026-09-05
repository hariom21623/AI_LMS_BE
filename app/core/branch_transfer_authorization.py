from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


def _get_user_role_codes(
    db: Session,
    user_id: int,
) -> set[str]:
    rows = (
        db.query(Role.code)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )

    return {row[0] for row in rows}


def _is_super_admin(
    db: Session,
    user_id: int,
) -> bool:
    return "SUPER_ADMIN" in _get_user_role_codes(db, user_id)


def require_branch_transfer_access(
    db: Session,
    current_user: User,
    branch_id: int,
    target_institute_id: int,
) -> None:
    """
    Authorization rules for branch transfer.

    SUPER_ADMIN:
        Can transfer any branch to any institute.

    INSTITUTE_ADMIN:
        Can transfer a branch only when the branch currently
        belongs to their own institute.

    BRANCH_ADMIN / TEACHER / STUDENT:
        Cannot transfer branches.
    """

    role_codes = _get_user_role_codes(
        db,
        current_user.id,
    )

    # Super Admin → unrestricted
    if "SUPER_ADMIN" in role_codes:
        return

    # Only Super Admin and Institute Admin can transfer branches
    if "INSTITUTE_ADMIN" not in role_codes:
        raise AppException(
            "You do not have permission to transfer branches.",
            403,
            "PERMISSION_DENIED",
        )

    # Institute Admin must belong to an institute
    if current_user.institute_id is None:
        raise AppException(
            "Institute Admin is not assigned to an institute.",
            403,
            "INSTITUTE_ACCESS_DENIED",
        )

    # Get target branch
    from app.models.branch import Branch

    branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id)
        .first()
    )

    if not branch:
        raise AppException(
            "Branch not found.",
            404,
            "BRANCH_NOT_FOUND",
        )

    # Institute Admin can only transfer branches
    # currently belonging to their own institute
    if branch.institute_id != current_user.institute_id:
        raise AppException(
            "You do not have access to transfer this branch.",
            403,
            "INSTITUTE_ACCESS_DENIED",
        )