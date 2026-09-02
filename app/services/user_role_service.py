from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.repositories.user_role_repository import UserRoleRepository
from app.schemas.user_role import (
    RoleSummary,
    UserRoleAssignRequest,
    UserRoleResponse,
    UserSummary,
)


class UserRoleService:
    """
    Business logic related to assigning and managing
    roles for users.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRoleRepository(db)

    def assign_role(
        self,
        user_id: int,
        data: UserRoleAssignRequest,
    ) -> UserRoleResponse:
        """
        Assign a role to a user.
        """

        # -----------------------------------------------------
        # Check user
        # -----------------------------------------------------

        user = self.db.scalar(
            select(User).where(
                User.id == user_id
            )
        )

        if not user:
            raise AppException(
                message="User not found.",
                status_code=404,
                code="USER_NOT_FOUND",
            )

        # -----------------------------------------------------
        # Check role
        # -----------------------------------------------------

        role = self.db.scalar(
            select(Role).where(
                Role.id == data.role_id
            )
        )

        if not role:
            raise AppException(
                message="Role not found.",
                status_code=404,
                code="ROLE_NOT_FOUND",
            )

        if not role.is_active:
            raise AppException(
                message="Role is inactive.",
                status_code=400,
                code="ROLE_INACTIVE",
            )

        # -----------------------------------------------------
        # Prevent duplicate assignment
        # -----------------------------------------------------

        existing_assignment = (
            self.repository.get_by_user_and_role(
                user_id=user_id,
                role_id=data.role_id,
            )
        )

        if existing_assignment:
            raise AppException(
                message="This role is already assigned to the user.",
                status_code=409,
                code="ROLE_ALREADY_ASSIGNED",
            )

        # -----------------------------------------------------
        # Validate institute scope
        # -----------------------------------------------------

        if role.institute_id is not None:

            if user.institute_id != role.institute_id:
                raise AppException(
                    message=(
                        "This role belongs to a different institute."
                    ),
                    status_code=403,
                    code="ROLE_INSTITUTE_MISMATCH",
                )

        # -----------------------------------------------------
        # Create assignment
        # -----------------------------------------------------

        user_role = UserRole(
            user_id=user_id,
            role_id=data.role_id,
        )

        user_role = self.repository.create(
            user_role
        )

        self.db.commit()
        self.db.refresh(user_role)

        return UserRoleResponse(
            id=user_role.id,
            user=UserSummary(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
            ),
            role=RoleSummary(
                id=role.id,
                name=role.name,
                code=role.code,
            ),
        )

    def get_user_roles(
        self,
        user_id: int,
    ) -> list[UserRoleResponse]:
        """
        Get all roles assigned to a user with
        user and role details.
        """

        user = self.db.scalar(
            select(User).where(
                User.id == user_id
            )
        )

        if not user:
            raise AppException(
                message="User not found.",
                status_code=404,
                code="USER_NOT_FOUND",
            )

        assignments = self.repository.get_roles_by_user(
            user_id
        )

        return [
            UserRoleResponse(
                id=user_role.id,
                user=UserSummary(
                    id=assigned_user.id,
                    full_name=assigned_user.full_name,
                    email=assigned_user.email,
                ),
                role=RoleSummary(
                    id=role.id,
                    name=role.name,
                    code=role.code,
                ),
            )
            for user_role, assigned_user, role in assignments
        ]

    def revoke_role(
        self,
        user_id: int,
        role_id: int,
    ) -> None:
        """
        Revoke a role from a user.
        """

        user = self.db.scalar(
            select(User).where(
                User.id == user_id
            )
        )

        if not user:
            raise AppException(
                message="User not found.",
                status_code=404,
                code="USER_NOT_FOUND",
            )

        user_role = (
            self.repository.get_by_user_and_role(
                user_id=user_id,
                role_id=role_id,
            )
        )

        if not user_role:
            raise AppException(
                message="Role assignment not found.",
                status_code=404,
                code="ROLE_ASSIGNMENT_NOT_FOUND",
            )

        self.repository.delete(user_role)

        self.db.commit()