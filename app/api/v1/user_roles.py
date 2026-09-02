from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_role import (
    UserRoleAssignRequest,
    UserRoleResponse,
)
from app.services.user_role_service import UserRoleService


router = APIRouter(
    prefix="/users",
    tags=["User Roles"],
)


@router.post(
    "/{user_id}/roles",
    response_model=UserRoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_role(
    user_id: int,
    data: UserRoleAssignRequest,
    current_user: User = Depends(
        require_permission("user:role:assign")
    ),
    db: Session = Depends(get_db),
):
    """
    Assign a role to a user.

    Requires:
        user:role:assign
    """

    service = UserRoleService(db)

    return service.assign_role(
        user_id=user_id,
        data=data,
    )


@router.get(
    "/{user_id}/roles",
    response_model=list[UserRoleResponse],
)
def get_user_roles(
    user_id: int,
    current_user: User = Depends(
        require_permission("user:role:read")
    ),
    db: Session = Depends(get_db),
):
    """
    Get all roles assigned to a user.

    Requires:
        user:role:read
    """

    service = UserRoleService(db)

    return service.get_user_roles(
        user_id=user_id,
    )


@router.delete(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def revoke_role(
    user_id: int,
    role_id: int,
    current_user: User = Depends(
        require_permission("user:role:revoke")
    ),
    db: Session = Depends(get_db),
):
    """
    Revoke a role from a user.

    Requires:
        user:role:revoke
    """

    service = UserRoleService(db)

    service.revoke_role(
        user_id=user_id,
        role_id=role_id,
    )

    return None