from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


class UserRoleRepository:
    """
    Database operations related to UserRole.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_and_role(
        self,
        user_id: int,
        role_id: int,
    ) -> UserRole | None:
        """
        Get a specific user-role assignment.
        """

        stmt = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        )

        return self.db.scalar(stmt)

    def get_roles_by_user(
        self,
        user_id: int,
    ) -> list[tuple[UserRole, User, Role]]:
        """
        Get all role assignments for a user along with
        user and role details.
        """

        stmt = (
            select(UserRole, User, Role)
            .join(
                User,
                User.id == UserRole.user_id,
            )
            .join(
                Role,
                Role.id == UserRole.role_id,
            )
            .where(
                UserRole.user_id == user_id,
            )
            .order_by(
                UserRole.id.asc()
            )
        )

        return list(self.db.execute(stmt).all())

    def create(
        self,
        user_role: UserRole,
    ) -> UserRole:
        """
        Create a new user-role assignment.
        """

        self.db.add(user_role)
        self.db.flush()
        self.db.refresh(user_role)

        return user_role

    def delete(
        self,
        user_role: UserRole,
    ) -> None:
        """
        Delete a user-role assignment.
        """

        self.db.delete(user_role)
        self.db.flush()