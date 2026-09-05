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
    stmt = (
        select(Role.code)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(
            UserRole.user_id == user_id,
            Role.is_active.is_(True),
        )
    )

    return set(db.scalars(stmt).all())


def _is_super_admin(
    db: Session,
    user: User,
) -> bool:
    role_codes = _get_user_role_codes(
        db,
        user.id,
    )

    return "SUPER_ADMIN" in role_codes


def _get_target_user(
    db: Session,
    user_id: int,
) -> User:
    target_user = db.scalar(
        select(User).where(
            User.id == user_id,
        )
    )

    if not target_user:
        raise AppException(
            "User not found.",
            404,
            "USER_NOT_FOUND",
        )

    return target_user


def _get_role_by_id(
    db: Session,
    role_id: int,
) -> Role:
    role = db.scalar(
        select(Role).where(
            Role.id == role_id,
            Role.is_active.is_(True),
        )
    )

    if not role:
        raise AppException(
            "Role not found or inactive.",
            404,
            "ROLE_NOT_FOUND",
        )

    return role


def require_user_create_access(
    institute_id: int,
    branch_id: int | None,
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    role = _get_role_by_id(
        db,
        role_id,
    )

    role_code = role.code

    if role_code == "SUPER_ADMIN":
        raise AppException(
            "SUPER_ADMIN cannot be created through user management.",
            403,
            "SUPER_ADMIN_CREATION_NOT_ALLOWED",
        )

    if _is_super_admin(db, current_user):
        return current_user

    current_roles = _get_user_role_codes(
        db,
        current_user.id,
    )

    # Institute Admin
    if "INSTITUTE_ADMIN" in current_roles:

        if current_user.institute_id != institute_id:
            raise AppException(
                "You do not have access to this institute.",
                403,
                "INSTITUTE_ACCESS_DENIED",
            )

        allowed_roles = {
            "BRANCH_ADMIN",
            "TEACHER",
            "STUDENT",
        }

        if role_code not in allowed_roles:
            raise AppException(
                "Institute Admin cannot create this role.",
                403,
                "ROLE_CREATION_DENIED",
            )

        return current_user

    # Branch Admin
    if "BRANCH_ADMIN" in current_roles:

        if (
            current_user.institute_id != institute_id
            or current_user.branch_id is None
            or branch_id != current_user.branch_id
        ):
            raise AppException(
                "You can only create users in your own branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )

        allowed_roles = {
            "TEACHER",
            "STUDENT",
        }

        if role_code not in allowed_roles:
            raise AppException(
                "Branch Admin can only create Teacher or Student.",
                403,
                "ROLE_CREATION_DENIED",
            )

        return current_user

    raise AppException(
        "You do not have access to user management.",
        403,
        "USER_ACCESS_DENIED",
    )


def require_user_read_access(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    target_user = _get_target_user(
        db,
        user_id,
    )

    if _is_super_admin(db, current_user):
        return current_user

    role_codes = _get_user_role_codes(
        db,
        current_user.id,
    )

    # Institute Admin
    if "INSTITUTE_ADMIN" in role_codes:

        if (
            current_user.institute_id is None
            or target_user.institute_id
            != current_user.institute_id
        ):
            raise AppException(
                "You do not have access to this user.",
                403,
                "USER_ACCESS_DENIED",
            )

        return current_user

    # Branch Admin
    if "BRANCH_ADMIN" in role_codes:

        if (
            current_user.institute_id is None
            or current_user.branch_id is None
            or target_user.institute_id
            != current_user.institute_id
            or target_user.branch_id
            != current_user.branch_id
        ):
            raise AppException(
                "You do not have access to this user.",
                403,
                "USER_ACCESS_DENIED",
            )

        return current_user

    raise AppException(
        "You do not have access to user management.",
        403,
        "USER_ACCESS_DENIED",
    )


def require_user_update_access(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    target_user = _get_target_user(
        db,
        user_id,
    )

    if _is_super_admin(db, current_user):
        return current_user

    role_codes = _get_user_role_codes(
        db,
        current_user.id,
    )

    # Institute Admin
    if "INSTITUTE_ADMIN" in role_codes:

        if (
            current_user.institute_id is None
            or target_user.institute_id
            != current_user.institute_id
        ):
            raise AppException(
                "You do not have access to update this user.",
                403,
                "USER_ACCESS_DENIED",
            )

        return current_user

    # Branch Admin
    if "BRANCH_ADMIN" in role_codes:

        if (
            current_user.institute_id is None
            or current_user.branch_id is None
            or target_user.institute_id
            != current_user.institute_id
            or target_user.branch_id
            != current_user.branch_id
        ):
            raise AppException(
                "You can only update users in your own branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )

        return current_user

    raise AppException(
        "You do not have permission to update users.",
        403,
        "USER_ACCESS_DENIED",
    )


def require_user_delete_access(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    target_user = _get_target_user(
        db,
        user_id,
    )

    if _is_super_admin(db, current_user):
        return current_user

    current_roles = _get_user_role_codes(
        db,
        current_user.id,
    )

    target_roles = _get_user_role_codes(
        db,
        target_user.id,
    )

    # Institute Admin
    if "INSTITUTE_ADMIN" in current_roles:

        if (
            current_user.institute_id is None
            or target_user.institute_id
            != current_user.institute_id
        ):
            raise AppException(
                "You do not have access to delete this user.",
                403,
                "USER_ACCESS_DENIED",
            )

        if "INSTITUTE_ADMIN" in target_roles:
            raise AppException(
                "Institute Admin cannot delete another Institute Admin.",
                403,
                "ROLE_DELETE_DENIED",
            )

        if "SUPER_ADMIN" in target_roles:
            raise AppException(
                "SUPER_ADMIN cannot be deleted through user management.",
                403,
                "SUPER_ADMIN_DELETE_DENIED",
            )

        return current_user

    # Branch Admin
    if "BRANCH_ADMIN" in current_roles:

        if (
            current_user.institute_id is None
            or current_user.branch_id is None
            or target_user.institute_id
            != current_user.institute_id
            or target_user.branch_id
            != current_user.branch_id
        ):
            raise AppException(
                "You can only delete users in your own branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )

        if (
            "BRANCH_ADMIN" in target_roles
            or "INSTITUTE_ADMIN" in target_roles
            or "SUPER_ADMIN" in target_roles
        ):
            raise AppException(
                "Branch Admin cannot delete administrative users.",
                403,
                "ROLE_DELETE_DENIED",
            )

        return current_user

    raise AppException(
        "You do not have permission to delete users.",
        403,
        "USER_ACCESS_DENIED",
    )


def require_institute_user_access(
    institute_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    if _is_super_admin(db, current_user):
        return current_user

    role_codes = _get_user_role_codes(
        db,
        current_user.id,
    )

    if "INSTITUTE_ADMIN" in role_codes:

        if current_user.institute_id != institute_id:
            raise AppException(
                "You do not have access to this institute.",
                403,
                "INSTITUTE_ACCESS_DENIED",
            )

        return current_user

    raise AppException(
        "Only Super Admin or Institute Admin can access institute users.",
        403,
        "USER_ACCESS_DENIED",
    )


def require_branch_user_access(
    branch_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    branch = db.scalar(
        select(Branch).where(
            Branch.id == branch_id,
        )
    )

    if not branch:
        raise AppException(
            "Branch not found.",
            404,
            "BRANCH_NOT_FOUND",
        )

    if _is_super_admin(db, current_user):
        return current_user

    role_codes = _get_user_role_codes(
        db,
        current_user.id,
    )

    # Institute Admin
    if "INSTITUTE_ADMIN" in role_codes:

        if current_user.institute_id != branch.institute_id:
            raise AppException(
                "You do not have access to this branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )

        return current_user

    # Branch Admin
    if "BRANCH_ADMIN" in role_codes:

        if (
            current_user.institute_id != branch.institute_id
            or current_user.branch_id != branch.id
        ):
            raise AppException(
                "You do not have access to this branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )

        return current_user

    raise AppException(
        "You do not have access to user management.",
        403,
        "USER_ACCESS_DENIED",
    )