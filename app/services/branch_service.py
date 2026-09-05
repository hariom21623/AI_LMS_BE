from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.branch import Branch
from app.models.institute import Institute
from app.repositories.branch_repository import BranchRepository
from app.schemas.branch import BranchCreate, BranchUpdate


class BranchService:
    """
    Business logic related to Branch.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = BranchRepository(db)

    def create_branch(
        self,
        data: BranchCreate,
    ) -> Branch:
        """
        Create a new branch under an existing institute.
        """

        # Normalize values
        branch_code = data.code.strip().upper()

        branch_name = data.name.strip()

        branch_email = (
            data.email.lower().strip()
            if data.email
            else None
        )

        branch_phone = (
            data.phone.strip()
            if data.phone
            else None
        )

        branch_address = (
            data.address.strip()
            if data.address
            else None
        )

        branch_timezone = data.timezone.strip()

        # Check institute
        institute = self.db.scalar(
            select(Institute).where(
                Institute.id == data.institute_id
            )
        )

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        # Do not create branch under inactive institute
        if not institute.is_active:
            raise AppException(
                message="Cannot create a branch under an inactive institute.",
                status_code=400,
                code="INSTITUTE_INACTIVE",
            )

        # Check duplicate branch code
        existing_branch = self.repository.get_by_code(
            institute_id=data.institute_id,
            code=branch_code,
        )

        if existing_branch:
            raise AppException(
                message="A branch with this code already exists in this institute.",
                status_code=409,
                code="BRANCH_CODE_ALREADY_EXISTS",
            )

        # Create branch
        branch = Branch(
            institute_id=data.institute_id,
            name=branch_name,
            code=branch_code,
            email=branch_email,
            phone=branch_phone,
            address=branch_address,
            timezone=branch_timezone,
            is_active=True,
        )

        branch = self.repository.create(branch)

        self.db.commit()
        self.db.refresh(branch)

        return branch

    def get_branch(
        self,
        branch_id: int,
    ) -> Branch:
        """
        Get a branch by ID.
        """

        branch = self.repository.get_by_id(
            branch_id
        )

        if not branch:
            raise AppException(
                message="Branch not found.",
                status_code=404,
                code="BRANCH_NOT_FOUND",
            )

        return branch

    def get_all_branches(
        self,
        institute_id: int,
    ) -> list[Branch]:
        """
        Get all branches belonging to an institute.
        """

        institute = self.db.scalar(
            select(Institute).where(
                Institute.id == institute_id
            )
        )

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        return self.repository.get_all_by_institute(
            institute_id
        )

    def update_branch(
        self,
        branch_id: int,
        data: BranchUpdate,
    ) -> Branch:
        """
        Update an existing branch.
        """

        branch = self.repository.get_by_id(
            branch_id
        )

        if not branch:
            raise AppException(
                message="Branch not found.",
                status_code=404,
                code="BRANCH_NOT_FOUND",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Normalize code
        if "code" in update_data:
            if update_data["code"]:
                new_code = (
                    update_data["code"]
                    .strip()
                    .upper()
                )

                existing_branch = (
                    self.repository.get_by_code(
                        institute_id=branch.institute_id,
                        code=new_code,
                    )
                )

                if (
                    existing_branch
                    and existing_branch.id != branch.id
                ):
                    raise AppException(
                        message="A branch with this code already exists in this institute.",
                        status_code=409,
                        code="BRANCH_CODE_ALREADY_EXISTS",
                    )

                update_data["code"] = new_code

        # Normalize string fields
        string_fields = [
            "name",
            "phone",
            "address",
            "timezone",
        ]

        for field in string_fields:
            if field in update_data:
                value = update_data[field]

                if value is not None:
                    update_data[field] = value.strip()

        # Normalize email
        if "email" in update_data:
            if update_data["email"]:
                update_data["email"] = (
                    update_data["email"]
                    .lower()
                    .strip()
                )
            else:
                update_data["email"] = None

        # Apply updates
        for field, value in update_data.items():
            setattr(
                branch,
                field,
                value,
            )

        branch = self.repository.update(
            branch
        )

        self.db.commit()
        self.db.refresh(branch)

        return branch

    def delete_branch(
        self,
        branch_id: int,
    ) -> None:
        """
        Delete a branch.
        """

        branch = self.repository.get_by_id(
            branch_id
        )

        if not branch:
            raise AppException(
                message="Branch not found.",
                status_code=404,
                code="BRANCH_NOT_FOUND",
            )

        self.repository.delete(branch)

        self.db.commit()