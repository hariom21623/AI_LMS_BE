from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.branch_authorization import (
    require_branch_access,
    require_branch_create_access,
    require_institute_branch_read_access,
)
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.branch import (
    BranchCreate,
    BranchResponse,
    BranchUpdate,
)
from app.services.branch_service import BranchService


router = APIRouter(
    prefix="/branches",
    tags=["Branches"],
)


@router.post(
    "",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_branch(
    data: BranchCreate,
    current_user: User = Depends(
        require_permission("branch:create")
    ),
    db: Session = Depends(get_db),
):
    # Verify that the current user can create
    # a branch under the requested institute.
    require_branch_create_access(
        institute_id=data.institute_id,
        current_user=current_user,
        db=db,
    )

    service = BranchService(db)

    return service.create_branch(
        data=data,
    )


@router.get(
    "/{branch_id}",
    response_model=BranchResponse,
)
def get_branch(
    branch_id: int,
    current_user: User = Depends(
        require_permission("branch:read")
    ),
    db: Session = Depends(get_db),
):
    # Verify access to this specific branch.
    require_branch_access(
        branch_id=branch_id,
        current_user=current_user,
        db=db,
    )

    service = BranchService(db)

    return service.get_branch(
        branch_id=branch_id,
    )


@router.get(
    "/institute/{institute_id}",
    response_model=list[BranchResponse],
)
def get_institute_branches(
    institute_id: int,
    current_user: User = Depends(
        require_permission("branch:read")
    ),
    db: Session = Depends(get_db),
):
    # Verify access to this institute before
    # returning its branches.
    require_institute_branch_read_access(
        institute_id=institute_id,
        current_user=current_user,
        db=db,
    )

    service = BranchService(db)

    return service.get_all_branches(
        institute_id=institute_id,
    )


@router.put(
    "/{branch_id}",
    response_model=BranchResponse,
)
def update_branch(
    branch_id: int,
    data: BranchUpdate,
    current_user: User = Depends(
        require_permission("branch:update")
    ),
    db: Session = Depends(get_db),
):
    # Verify access to this specific branch.
    require_branch_access(
        branch_id=branch_id,
        current_user=current_user,
        db=db,
    )

    service = BranchService(db)

    return service.update_branch(
        branch_id=branch_id,
        data=data,
    )


@router.delete(
    "/{branch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_branch(
    branch_id: int,
    current_user: User = Depends(
        require_permission("branch:delete")
    ),
    db: Session = Depends(get_db),
):
    # Verify access to this specific branch.
    require_branch_access(
        branch_id=branch_id,
        current_user=current_user,
        db=db,
    )

    service = BranchService(db)

    service.delete_branch(
        branch_id=branch_id,
    )

    return None