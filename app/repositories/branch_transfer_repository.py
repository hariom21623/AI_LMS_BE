from datetime import datetime

from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.models.branch_transfer_history import BranchTransferHistory
from app.models.user import User


class BranchTransferRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_branch_by_id(
        self,
        branch_id: int,
    ) -> Branch | None:
        return (
            self.db.query(Branch)
            .filter(Branch.id == branch_id)
            .first()
        )

    def get_institute_by_id(
        self,
        institute_id: int,
    ):
        from app.models.institute import Institute

        return (
            self.db.query(Institute)
            .filter(Institute.id == institute_id)
            .first()
        )

    def get_users_by_branch_id(
        self,
        branch_id: int,
    ) -> list[User]:
        return (
            self.db.query(User)
            .filter(User.branch_id == branch_id)
            .all()
        )

    def create_history(
        self,
        branch_id: int,
        from_institute_id: int,
        to_institute_id: int,
        reason: str | None,
        transferred_by: int,
    ) -> BranchTransferHistory:
        history = BranchTransferHistory(
            branch_id=branch_id,
            from_institute_id=from_institute_id,
            to_institute_id=to_institute_id,
            reason=reason,
            transferred_by=transferred_by,
        )

        self.db.add(history)
        self.db.flush()

        return history

    def get_history_by_id(
        self,
        history_id: int,
    ) -> BranchTransferHistory | None:
        return (
            self.db.query(BranchTransferHistory)
            .filter(BranchTransferHistory.id == history_id)
            .first()
        )

    def get_latest_transfer_history(
        self,
        branch_id: int,
    ) -> BranchTransferHistory | None:
        return (
            self.db.query(BranchTransferHistory)
            .filter(
                BranchTransferHistory.branch_id == branch_id,
                BranchTransferHistory.is_reversed.is_(False),
            )
            .order_by(
                BranchTransferHistory.transferred_at.desc()
            )
            .first()
        )

    def get_branch_transfer_history(
        self,
        branch_id: int,
    ) -> list[BranchTransferHistory]:
        return (
            self.db.query(BranchTransferHistory)
            .filter(
                BranchTransferHistory.branch_id == branch_id
            )
            .order_by(
                BranchTransferHistory.transferred_at.desc()
            )
            .all()
        )

    def mark_history_reversed(
        self,
        history: BranchTransferHistory,
        reversed_by: int,
        reversed_at: datetime,
    ) -> BranchTransferHistory:
        history.is_reversed = True
        history.reversed_by = reversed_by
        history.reversed_at = reversed_at

        self.db.flush()

        return history