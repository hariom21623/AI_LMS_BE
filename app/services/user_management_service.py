from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import hash_password
from app.models.branch import Branch
from app.models.institute import Institute
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.repositories.user_management_repository import (
    UserManagementRepository,
)
from app.schemas.user_management import (
    UserCreate,
    UserUpdate,
)


class UserManagementService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserManagementRepository(db)

    def _validate_institute(
        self,
        institute_id: int,
    ) -> Institute:
        institute = self.db.scalar(
            select(Institute).where(
                Institute.id == institute_id
            )
        )

        if not institute:
            raise AppException(
                "Institute not found.",
                404,
                "INSTITUTE_NOT_FOUND",
            )

        if not institute.is_active:
            raise AppException(
                "Institute is inactive.",
                400,
                "INSTITUTE_INACTIVE",
            )

        return institute

    def _validate_branch(
        self,
        branch_id: int,
        institute_id: int,
    ) -> Branch:
        branch = self.db.scalar(
            select(Branch).where(
                Branch.id == branch_id
            )
        )

        if not branch:
            raise AppException(
                "Branch not found.",
                404,
                "BRANCH_NOT_FOUND",
            )

        if not branch.is_active:
            raise AppException(
                "Branch is inactive.",
                400,
                "BRANCH_INACTIVE",
            )

        if branch.institute_id != institute_id:
            raise AppException(
                "Branch does not belong to this institute.",
                400,
                "BRANCH_INSTITUTE_MISMATCH",
            )

        return branch

    def _validate_role(
        self,
        role_id: int,
        institute_id: int,
    ) -> Role:
        role = self.repository.get_role_by_id(role_id)

        if not role:
            raise AppException(
                "Role not found or inactive.",
                404,
                "ROLE_NOT_FOUND",
            )

        if (
            role.institute_id is not None
            and role.institute_id != institute_id
        ):
            raise AppException(
                "This role does not belong to the requested institute.",
                400,
                "ROLE_INSTITUTE_MISMATCH",
            )

        return role

    def _validate_role_branch_requirement(
        self,
        role: Role,
        branch_id: int | None,
    ) -> None:
        branch_level_roles = {
            "BRANCH_ADMIN",
            "TEACHER",
            "STUDENT",
        }

        if (
            role.code in branch_level_roles
            and branch_id is None
        ):
            raise AppException(
                "A branch is required for this role.",
                400,
                "BRANCH_REQUIRED",
            )

        if (
            role.code == "INSTITUTE_ADMIN"
            and branch_id is not None
        ):
            raise AppException(
                "Institute Admin cannot be assigned to a branch.",
                400,
                "INSTITUTE_ADMIN_BRANCH_NOT_ALLOWED",
            )

        if role.code == "SUPER_ADMIN":
            raise AppException(
                "SUPER_ADMIN cannot be created through user management.",
                403,
                "SUPER_ADMIN_CREATION_NOT_ALLOWED",
            )

    def create_user(
        self,
        data: UserCreate,
    ) -> User:
        email = data.email.lower().strip()

        phone = (
            data.phone.strip()
            if data.phone
            else None
        )

        full_name = data.full_name.strip()
        timezone = data.timezone.strip()

        self._validate_institute(
            data.institute_id
        )

        if data.branch_id is not None:
            self._validate_branch(
                data.branch_id,
                data.institute_id,
            )

        role = self._validate_role(
            data.role_id,
            data.institute_id,
        )

        self._validate_role_branch_requirement(
            role,
            data.branch_id,
        )

        existing_email = (
            self.repository.get_user_by_email(email)
        )

        if existing_email:
            raise AppException(
                "A user with this email already exists.",
                409,
                "USER_EMAIL_ALREADY_EXISTS",
            )

        if phone:
            existing_phone = (
                self.repository.get_user_by_phone(phone)
            )

            if existing_phone:
                raise AppException(
                    "A user with this phone number already exists.",
                    409,
                    "USER_PHONE_ALREADY_EXISTS",
                )

        user = User(
            institute_id=data.institute_id,
            branch_id=data.branch_id,
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=hash_password(
                data.password
            ),
            is_active=True,
            is_verified=False,
            timezone=timezone,
        )

        user = self.repository.create_user(user)

        user_role = UserRole(
            user_id=user.id,
            role_id=role.id,
        )

        self.repository.create_user_role(
            user_role
        )

        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user(
        self,
        user_id: int,
    ) -> User:
        user = self.repository.get_user_by_id(
            user_id
        )

        if not user:
            raise AppException(
                "User not found.",
                404,
                "USER_NOT_FOUND",
            )

        return user

    def get_users_by_institute(
        self,
        institute_id: int,
    ) -> list[User]:
        self._validate_institute(
            institute_id
        )

        return self.repository.get_users_by_institute(
            institute_id
        )

    def get_users_by_branch(
        self,
        branch_id: int,
    ) -> list[User]:
        branch = self.db.scalar(
            select(Branch).where(
                Branch.id == branch_id
            )
        )

        if not branch:
            raise AppException(
                "Branch not found.",
                404,
                "BRANCH_NOT_FOUND",
            )

        return self.repository.get_users_by_branch(
            branch_id
        )

    def update_user(
        self,
        user_id: int,
        data: UserUpdate,
    ) -> User:
        user = self.repository.get_user_by_id(
            user_id
        )

        if not user:
            raise AppException(
                "User not found.",
                404,
                "USER_NOT_FOUND",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "full_name" in update_data:
            update_data["full_name"] = (
                update_data["full_name"].strip()
            )

        if "email" in update_data:
            new_email = (
                update_data["email"]
                .lower()
                .strip()
            )

            existing_email = (
                self.repository.get_user_by_email(
                    new_email
                )
            )

            if (
                existing_email
                and existing_email.id != user.id
            ):
                raise AppException(
                    "A user with this email already exists.",
                    409,
                    "USER_EMAIL_ALREADY_EXISTS",
                )

            update_data["email"] = new_email

        if "phone" in update_data:
            new_phone = (
                update_data["phone"].strip()
                if update_data["phone"]
                else None
            )

            if new_phone:
                existing_phone = (
                    self.repository.get_user_by_phone(
                        new_phone
                    )
                )

                if (
                    existing_phone
                    and existing_phone.id != user.id
                ):
                    raise AppException(
                        "A user with this phone number already exists.",
                        409,
                        "USER_PHONE_ALREADY_EXISTS",
                    )

            update_data["phone"] = new_phone

        if (
            "timezone" in update_data
            and update_data["timezone"]
        ):
            update_data["timezone"] = (
                update_data["timezone"].strip()
            )

        for field, value in update_data.items():
            setattr(
                user,
                field,
                value,
            )

        user = self.repository.update_user(
            user
        )

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(
        self,
        user_id: int,
    ) -> None:
        user = self.repository.get_user_by_id(
            user_id
        )

        if not user:
            raise AppException(
                "User not found.",
                404,
                "USER_NOT_FOUND",
            )

        self.repository.delete_user(user)

        self.db.commit()