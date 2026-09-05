from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.timezone import india_now
from app.repositories.branch_transfer_repository import (
    BranchTransferRepository,
)
from app.schemas.branch_transfer_reversal import (
    BranchTransferReversalRequest,
    BranchTransferReversalResponse,
)


class BranchTransferReversalService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BranchTransferRepository(db)

    def reverse_branch_transfer(
        self,
        branch_id: int,
        request: BranchTransferReversalRequest,
        reversed_by: int,
    ) -> BranchTransferReversalResponse:

        # 1. Get branch
        branch = self.repository.get_branch_by_id(branch_id)

        if not branch:
            raise AppException(
                "Branch not found.",
                404,
                "BRANCH_NOT_FOUND",
            )

        # 2. Get latest active transfer
        history = self.repository.get_latest_transfer_history(
            branch_id
        )

        if not history:
            raise AppException(
                "No active transfer history found for this branch.",
                404,
                "TRANSFER_HISTORY_NOT_FOUND",
            )

        # 3. Validate current branch state
        if branch.institute_id != history.to_institute_id:
            raise AppException(
                "Branch state does not match the latest transfer history.",
                409,
                "TRANSFER_STATE_MISMATCH",
            )

        # 4. Get users belonging to branch
        branch_users = self.repository.get_users_by_branch_id(
            branch_id
        )

        try:
            # 5. Restore branch to previous institute
            branch.institute_id = history.from_institute_id

            # 6. Restore all branch users
            for user in branch_users:
                user.institute_id = history.from_institute_id

            # 7. Mark original history as reversed
            self.repository.mark_history_reversed(
                history=history,
                reversed_by=reversed_by,
                reversed_at=india_now(),
            )

            # 8. Add reversal reason if provided
            if request.reason:
                original_reason = history.reason or ""

                history.reason = (
                    f"{original_reason} | "
                    f"Reversal: {request.reason}"
                )

            # 9. Commit everything together
            self.db.commit()

            # 10. Refresh history
            self.db.refresh(history)

            return BranchTransferReversalResponse.model_validate(
                history
            )

        except Exception:
            self.db.rollback()
            raise