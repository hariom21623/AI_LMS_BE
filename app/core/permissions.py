from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.database import get_db
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_role import UserRole


def require_permission(permission_code: str):
    """
    Create a FastAPI dependency that checks whether the
    current user has the required permission.

    Permissions are resolved dynamically from the database.
    """

    def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        """
        Check the current user's roles and permissions.
        """

        stmt = (
            select(Permission.id)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .join(
                Role,
                Role.id == RolePermission.role_id,
            )
            .join(
                UserRole,
                UserRole.role_id == Role.id,
            )
            .where(
                UserRole.user_id == current_user.id,
                Permission.code == permission_code,
                Permission.is_active.is_(True),
                Role.is_active.is_(True),
            )
        )

        permission_id = db.scalar(stmt)

        if permission_id is None:
            raise AppException(
                message="You do not have permission to perform this action.",
                status_code=403,
                code="PERMISSION_DENIED",
            )

        return current_user

    return permission_dependency