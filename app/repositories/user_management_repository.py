from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


class UserManagementRepository:
    """
    Database operations related to User Management.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Get a user by ID.
        """

        stmt = select(User).where(
            User.id == user_id
        )

        return self.db.scalar(stmt)

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Get a user by email.
        """

        stmt = select(User).where(
            User.email == email
        )

        return self.db.scalar(stmt)

    def get_user_by_phone(
        self,
        phone: str,
    ) -> User | None:
        """
        Get a user by phone number.
        """

        stmt = select(User).where(
            User.phone == phone
        )

        return self.db.scalar(stmt)

    def get_users_by_institute(
        self,
        institute_id: int,
    ) -> list[User]:
        """
        Get all users belonging to an institute.
        """

        stmt = (
            select(User)
            .where(
                User.institute_id == institute_id
            )
            .order_by(User.id.asc())
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_users_by_branch(
        self,
        branch_id: int,
    ) -> list[User]:
        """
        Get all users belonging to a branch.
        """

        stmt = (
            select(User)
            .where(
                User.branch_id == branch_id
            )
            .order_by(User.id.asc())
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_role_by_id(
        self,
        role_id: int,
    ) -> Role | None:
        """
        Get an active role by ID.
        """

        stmt = select(Role).where(
            Role.id == role_id,
            Role.is_active.is_(True),
        )

        return self.db.scalar(stmt)

    def get_user_role(
        self,
        user_id: int,
        role_id: int,
    ) -> UserRole | None:
        """
        Get an existing user-role assignment.
        """

        stmt = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        )

        return self.db.scalar(stmt)

    def create_user(
        self,
        user: User,
    ) -> User:
        """
        Create a new user.
        """

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user

    def create_user_role(
        self,
        user_role: UserRole,
    ) -> UserRole:
        """
        Create a user-role assignment.
        """

        self.db.add(user_role)
        self.db.flush()
        self.db.refresh(user_role)

        return user_role

    def update_user(
        self,
        user: User,
    ) -> User:
        """
        Update an existing user.
        """

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user

    def delete_user(
        self,
        user: User,
    ) -> None:
        """
        Delete a user.
        """

        self.db.delete(user)
        self.db.flush()