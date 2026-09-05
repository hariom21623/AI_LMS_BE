from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.role import Role
from app.models.user import User
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
    user: User,
) -> bool:
    return "SUPER_ADMIN" in _get_user_role_codes(db, user.id)


def require_course_create_access(
    db: Session,
    user: User,
    institute_id: int,
    branch_id: int,
) -> None:
    if _is_super_admin(db, user):
        return

    roles = _get_user_role_codes(db, user.id)

    if "INSTITUTE_ADMIN" in roles:
        if user.institute_id != institute_id:
            raise AppException(
                "You do not have access to this institute.",
                403,
                "INSTITUTE_ACCESS_DENIED",
            )
        return

    if "BRANCH_ADMIN" in roles:
        if (
            user.institute_id != institute_id
            or user.branch_id != branch_id
        ):
            raise AppException(
                "You do not have access to this branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )
        return

    raise AppException(
        "You do not have permission to create courses.",
        403,
        "PERMISSION_DENIED",
    )


def require_course_read_access(
    db: Session,
    user: User,
    institute_id: int,
    branch_id: int,
) -> None:
    if _is_super_admin(db, user):
        return

    roles = _get_user_role_codes(db, user.id)

    if user.institute_id != institute_id:
        raise AppException(
            "You do not have access to this institute.",
            403,
            "INSTITUTE_ACCESS_DENIED",
        )

    if "INSTITUTE_ADMIN" in roles:
        return

    if user.branch_id != branch_id:
        raise AppException(
            "You do not have access to this branch.",
            403,
            "BRANCH_ACCESS_DENIED",
        )

    if roles.intersection(
        {
            "BRANCH_ADMIN",
            "TEACHER",
            "STUDENT",
        }
    ):
        return

    raise AppException(
        "You do not have permission to view courses.",
        403,
        "PERMISSION_DENIED",
    )


def require_course_update_access(
    db: Session,
    user: User,
    institute_id: int,
    branch_id: int,
) -> None:
    if _is_super_admin(db, user):
        return

    roles = _get_user_role_codes(db, user.id)

    if "INSTITUTE_ADMIN" in roles:
        if user.institute_id != institute_id:
            raise AppException(
                "You do not have access to this institute.",
                403,
                "INSTITUTE_ACCESS_DENIED",
            )
        return

    if "BRANCH_ADMIN" in roles:
        if (
            user.institute_id != institute_id
            or user.branch_id != branch_id
        ):
            raise AppException(
                "You do not have access to this branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )
        return

    raise AppException(
        "You do not have permission to update courses.",
        403,
        "PERMISSION_DENIED",
    )


def require_course_delete_access(
    db: Session,
    user: User,
    institute_id: int,
    branch_id: int,
) -> None:
    if _is_super_admin(db, user):
        return

    roles = _get_user_role_codes(db, user.id)

    if "INSTITUTE_ADMIN" in roles:
        if user.institute_id != institute_id:
            raise AppException(
                "You do not have access to this institute.",
                403,
                "INSTITUTE_ACCESS_DENIED",
            )
        return

    if "BRANCH_ADMIN" in roles:
        if (
            user.institute_id != institute_id
            or user.branch_id != branch_id
        ):
            raise AppException(
                "You do not have access to this branch.",
                403,
                "BRANCH_ACCESS_DENIED",
            )
        return

    raise AppException(
        "You do not have permission to delete courses.",
        403,
        "PERMISSION_DENIED",
    )