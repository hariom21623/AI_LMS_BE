from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.institute import Institute
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


class InstituteRepository:
    """
    Database operations related to Institute.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        institute_id: int,
    ) -> Institute | None:
        """
        Get an institute by ID.
        """

        stmt = select(Institute).where(
            Institute.id == institute_id
        )

        return self.db.scalar(stmt)

    def get_by_code(
        self,
        code: str,
    ) -> Institute | None:
        """
        Get an institute by unique code.
        """

        stmt = select(Institute).where(
            Institute.code == code
        )

        return self.db.scalar(stmt)

    def get_by_email(
        self,
        email: str,
    ) -> Institute | None:
        """
        Get an institute by email.
        """

        stmt = select(Institute).where(
            Institute.email == email
        )

        return self.db.scalar(stmt)

    def get_all(
        self,
    ) -> list[Institute]:
        """
        Get all institutes.
        """

        stmt = (
            select(Institute)
            .order_by(Institute.id.asc())
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_admin_by_institute_id(
        self,
        institute_id: int,
    ) -> User | None:
        """
        Get the active Institute Admin
        assigned to an institute.
        """

        stmt = (
            select(User)
            .join(
                UserRole,
                UserRole.user_id == User.id,
            )
            .join(
                Role,
                Role.id == UserRole.role_id,
            )
            .where(
                User.institute_id == institute_id,
                User.branch_id.is_(None),
                User.is_active.is_(True),
                Role.code == "INSTITUTE_ADMIN",
                Role.is_active.is_(True),
            )
            .order_by(User.id.asc())
            .limit(1)
        )

        return self.db.scalar(stmt)

    def create(
        self,
        institute: Institute,
    ) -> Institute:
        """
        Create a new institute.
        """

        self.db.add(institute)
        self.db.flush()
        self.db.refresh(institute)

        return institute

    def update(
        self,
        institute: Institute,
    ) -> Institute:
        """
        Update an existing institute.
        """

        self.db.add(institute)
        self.db.flush()
        self.db.refresh(institute)

        return institute

    def delete(
        self,
        institute: Institute,
    ) -> None:
        """
        Delete an institute.
        """

        self.db.delete(institute)
        self.db.flush()