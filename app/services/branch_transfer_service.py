from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.repositories.branch_transfer_repository import (
    BranchTransferRepository,
)
from app.schemas.branch_transfer import (
    BranchTransferRequest,
    BranchTransferResponse,
)


class BranchTransferService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BranchTransferRepository(db)

    def transfer_branch(
        self,
        branch_id: int,
        request: BranchTransferRequest,
        transferred_by: int,
    ) -> BranchTransferResponse:

        # 1. Get source branch
        branch = self.repository.get_branch_by_id(branch_id)

        if not branch:
            raise AppException(
                "Branch not found.",
                404,
                "BRANCH_NOT_FOUND",
            )

        # 2. Branch must be active
        if not branch.is_active:
            raise AppException(
                "Inactive branch cannot be transferred.",
                400,
                "BRANCH_INACTIVE",
            )

        # 3. Get target institute
        target_institute = self.repository.get_institute_by_id(
            request.to_institute_id
        )

        if not target_institute:
            raise AppException(
                "Target institute not found.",
                404,
                "TARGET_INSTITUTE_NOT_FOUND",
            )

        # 4. Target institute must be active
        if not target_institute.is_active:
            raise AppException(
                "Target institute is inactive.",
                400,
                "TARGET_INSTITUTE_INACTIVE",
            )

        # 5. Cannot transfer to same institute
        if branch.institute_id == request.to_institute_id:
            raise AppException(
                "Branch is already part of the target institute.",
                400,
                "SAME_INSTITUTE_TRANSFER",
            )

        from_institute_id = branch.institute_id

        try:
            # 6. Get all users belonging to this branch
            branch_users = self.repository.get_users_by_branch_id(
                branch_id
            )

            # 7. Update branch's institute
            branch.institute_id = request.to_institute_id

            # 8. Keep all branch users aligned with new institute
            for user in branch_users:
                user.institute_id = request.to_institute_id

            # 9. Create transfer history
            history = self.repository.create_history(
                branch_id=branch.id,
                from_institute_id=from_institute_id,
                to_institute_id=request.to_institute_id,
                reason=request.reason,
                transferred_by=transferred_by,
            )

            # 10. Commit branch + users + history together
            self.db.commit()

            # 11. Refresh history after commit
            self.db.refresh(history)

            return BranchTransferResponse.model_validate(history)

        except Exception:
            self.db.rollback()
            raise