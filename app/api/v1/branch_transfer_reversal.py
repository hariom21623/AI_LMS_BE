from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.branch_transfer_reversal_authorization import (
    require_branch_transfer_reversal_access,
)
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.branch_transfer_reversal import (
    BranchTransferReversalRequest,
    BranchTransferReversalResponse,
)
from app.services.branch_transfer_reversal_service import (
    BranchTransferReversalService,
)


router = APIRouter(
    prefix="/branches",
    tags=["Branch Transfer"],
)


@router.post(
    "/{branch_id}/transfer/reverse",
    response_model=BranchTransferReversalResponse,
    status_code=status.HTTP_200_OK,
)
def reverse_branch_transfer(
    branch_id: int,
    request: BranchTransferReversalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_branch_transfer_reversal_access(
        db=db,
        current_user=current_user,
        branch_id=branch_id,
    )

    service = BranchTransferReversalService(db)

    return service.reverse_branch_transfer(
        branch_id=branch_id,
        request=request,
        reversed_by=current_user.id,
    )