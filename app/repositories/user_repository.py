from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Database operations related to User.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
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

    def get_by_email(
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

    def get_by_phone(
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

    def create(
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

    def update(
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