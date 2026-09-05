from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.core.user_authorization import (
    require_branch_user_access,
    require_institute_user_access,
    require_user_create_access,
    require_user_delete_access,
    require_user_read_access,
    require_user_update_access,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_management import (
    UserCreate,
    UserManagementResponse,
    UserUpdate,
)
from app.services.user_management_service import (
    UserManagementService,
)


router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)


@router.post(
    "",
    response_model=UserManagementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
    current_user: User = Depends(
        require_permission("user:create")
    ),
    db: Session = Depends(get_db),
):
    """
    Create a user inside an institute/branch.
    """

    require_user_create_access(
        institute_id=data.institute_id,
        branch_id=data.branch_id,
        role_id=data.role_id,
        current_user=current_user,
        db=db,
    )

    service = UserManagementService(db)

    return service.create_user(
        data=data,
    )


@router.get(
    "/institute/{institute_id}",
    response_model=list[UserManagementResponse],
)
def get_institute_users(
    institute_id: int,
    current_user: User = Depends(
        require_permission("user:read")
    ),
    db: Session = Depends(get_db),
):
    """
    Get users belonging to an institute.
    """

    require_institute_user_access(
        institute_id=institute_id,
        current_user=current_user,
        db=db,
    )

    service = UserManagementService(db)

    return service.get_users_by_institute(
        institute_id=institute_id,
    )


@router.get(
    "/branch/{branch_id}",
    response_model=list[UserManagementResponse],
)
def get_branch_users(
    branch_id: int,
    current_user: User = Depends(
        require_permission("user:read")
    ),
    db: Session = Depends(get_db),
):
    """
    Get users belonging to a branch.
    """

    require_branch_user_access(
        branch_id=branch_id,
        current_user=current_user,
        db=db,
    )

    service = UserManagementService(db)

    return service.get_users_by_branch(
        branch_id=branch_id,
    )


@router.get(
    "/{user_id}",
    response_model=UserManagementResponse,
)
def get_user(
    user_id: int,
    current_user: User = Depends(
        require_permission("user:read")
    ),
    db: Session = Depends(get_db),
):
    """
    Get a specific user.
    """

    require_user_read_access(
        user_id=user_id,
        current_user=current_user,
        db=db,
    )

    service = UserManagementService(db)

    return service.get_user(
        user_id=user_id,
    )


@router.put(
    "/{user_id}",
    response_model=UserManagementResponse,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(
        require_permission("user:update")
    ),
    db: Session = Depends(get_db),
):
    """
    Update a user.
    """

    require_user_update_access(
        user_id=user_id,
        current_user=current_user,
        db=db,
    )

    service = UserManagementService(db)

    return service.update_user(
        user_id=user_id,
        data=data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    current_user: User = Depends(
        require_permission("user:delete")
    ),
    db: Session = Depends(get_db),
):
    """
    Delete a user.
    """

    require_user_delete_access(
        user_id=user_id,
        current_user=current_user,
        db=db,
    )

    service = UserManagementService(db)

    service.delete_user(
        user_id=user_id,
    )

    return None