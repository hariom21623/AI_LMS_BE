from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.branch_transfer_authorization import (
    require_branch_transfer_access,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.branch_transfer import (
    BranchTransferRequest,
    BranchTransferResponse,
)
from app.services.branch_transfer_service import (
    BranchTransferService,
)

router = APIRouter(
    prefix="/branches",
    tags=["Branch Transfer"],
)


@router.post(
    "/{branch_id}/transfer",
    response_model=BranchTransferResponse,
    status_code=status.HTTP_200_OK,
)
def transfer_branch(
    branch_id: int,
    request: BranchTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_branch_transfer_access(
        db=db,
        current_user=current_user,
        branch_id=branch_id,
        target_institute_id=request.to_institute_id,
    )

    service = BranchTransferService(db)

    return service.transfer_branch(
        branch_id=branch_id,
        request=request,
        transferred_by=current_user.id,
    )