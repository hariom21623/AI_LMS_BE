from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.branch import Branch


class BranchRepository:
    """
    Database operations related to Branch.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        branch_id: int,
    ) -> Branch | None:
        """
        Get a branch by ID.
        """

        stmt = select(Branch).where(
            Branch.id == branch_id
        )

        return self.db.scalar(stmt)

    def get_by_code(
        self,
        institute_id: int,
        code: str,
    ) -> Branch | None:
        """
        Get a branch by code within an institute.

        Branch code is unique per institute.
        """

        stmt = select(Branch).where(
            Branch.institute_id == institute_id,
            Branch.code == code,
        )

        return self.db.scalar(stmt)

    def get_all_by_institute(
        self,
        institute_id: int,
    ) -> list[Branch]:
        """
        Get all branches belonging to an institute.
        """

        stmt = (
            select(Branch)
            .where(
                Branch.institute_id == institute_id
            )
            .order_by(Branch.id.asc())
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def create(
        self,
        branch: Branch,
    ) -> Branch:
        """
        Create a new branch.
        """

        self.db.add(branch)
        self.db.flush()
        self.db.refresh(branch)

        return branch

    def update(
        self,
        branch: Branch,
    ) -> Branch:
        """
        Update an existing branch.
        """

        self.db.add(branch)
        self.db.flush()
        self.db.refresh(branch)

        return branch

    def delete(
        self,
        branch: Branch,
    ) -> None:
        """
        Delete a branch.
        """

        self.db.delete(branch)
        self.db.flush()