from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import hash_password
from app.models.institute import Institute
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.repositories.institute_repository import InstituteRepository
from app.schemas.institute import InstituteCreate, InstituteUpdate


class InstituteService:
    """
    Business logic related to Institute.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = InstituteRepository(db)

    def _build_institute_response(
        self,
        institute: Institute,
    ) -> dict:
        """
        Build institute response with its
        Institute Admin details.
        """

        admin_user = (
            self.repository.get_admin_by_institute_id(
                institute.id
            )
        )

        return {
            "id": institute.id,
            "name": institute.name,
            "code": institute.code,
            "email": institute.email,
            "phone": institute.phone,
            "address": institute.address,
            "logo_url": institute.logo_url,
            "country_code": institute.country_code,
            "timezone": institute.timezone,
            "is_active": institute.is_active,
            "admin": (
                {
                    "id": admin_user.id,
                    "full_name": admin_user.full_name,
                    "email": admin_user.email,
                    "phone": admin_user.phone,
                    "institute_id": admin_user.institute_id,
                    "branch_id": admin_user.branch_id,
                    "is_active": admin_user.is_active,
                    "is_verified": admin_user.is_verified,
                }
                if admin_user
                else None
            ),
        }

    def create_institute(
        self,
        data: InstituteCreate,
    ) -> dict:
        """
        Create an institute together with its
        initial Institute Admin.
        """

        institute_code = data.code.strip().upper()

        institute_email = (
            data.email.lower().strip()
            if data.email
            else None
        )

        # -------------------------------------------------
        # Check duplicate institute code
        # -------------------------------------------------

        existing_code = self.repository.get_by_code(
            institute_code
        )

        if existing_code:
            raise AppException(
                message="An institute with this code already exists.",
                status_code=409,
                code="INSTITUTE_CODE_ALREADY_EXISTS",
            )

        # -------------------------------------------------
        # Check duplicate institute email
        # -------------------------------------------------

        if institute_email:
            existing_email = self.repository.get_by_email(
                institute_email
            )

            if existing_email:
                raise AppException(
                    message="An institute with this email already exists.",
                    status_code=409,
                    code="INSTITUTE_EMAIL_ALREADY_EXISTS",
                )

        # -------------------------------------------------
        # Normalize admin details
        # -------------------------------------------------

        admin_email = data.admin.email.lower().strip()

        admin_phone = (
            data.admin.phone.strip()
            if data.admin.phone
            else None
        )

        # -------------------------------------------------
        # Check duplicate admin email
        # -------------------------------------------------

        existing_admin_email = self.db.scalar(
            select(User).where(
                User.email == admin_email
            )
        )

        if existing_admin_email:
            raise AppException(
                message="A user with this email already exists.",
                status_code=409,
                code="ADMIN_EMAIL_ALREADY_EXISTS",
            )

        # -------------------------------------------------
        # Check duplicate admin phone
        # -------------------------------------------------

        if admin_phone:
            existing_admin_phone = self.db.scalar(
                select(User).where(
                    User.phone == admin_phone
                )
            )

            if existing_admin_phone:
                raise AppException(
                    message="A user with this phone number already exists.",
                    status_code=409,
                    code="ADMIN_PHONE_ALREADY_EXISTS",
                )

        # -------------------------------------------------
        # Create Institute
        # -------------------------------------------------

        institute = Institute(
            name=data.name.strip(),
            code=institute_code,
            email=institute_email,
            phone=(
                data.phone.strip()
                if data.phone
                else None
            ),
            address=(
                data.address.strip()
                if data.address
                else None
            ),
            logo_url=(
                data.logo_url.strip()
                if data.logo_url
                else None
            ),
            country_code=data.country_code.upper(),
            timezone=data.timezone.strip(),
            is_active=True,
        )

        institute = self.repository.create(
            institute
        )

        # -------------------------------------------------
        # Create Initial Institute Admin
        # -------------------------------------------------

        admin_user = User(
            institute_id=institute.id,
            branch_id=None,
            full_name=data.admin.full_name.strip(),
            email=admin_email,
            phone=admin_phone,
            password_hash=hash_password(
                data.admin.password
            ),
            is_active=True,
            is_verified=False,
        )

        self.db.add(admin_user)
        self.db.flush()
        self.db.refresh(admin_user)

        # -------------------------------------------------
        # Get INSTITUTE_ADMIN role
        # -------------------------------------------------

        institute_admin_role = self.db.scalar(
            select(Role).where(
                Role.code == "INSTITUTE_ADMIN",
                Role.is_active.is_(True),
            )
        )

        if not institute_admin_role:
            self.db.rollback()

            raise AppException(
                message="INSTITUTE_ADMIN role is not configured.",
                status_code=500,
                code="INSTITUTE_ADMIN_ROLE_NOT_FOUND",
            )

        # -------------------------------------------------
        # Assign Institute Admin role
        # -------------------------------------------------

        user_role = UserRole(
            user_id=admin_user.id,
            role_id=institute_admin_role.id,
        )

        self.db.add(user_role)
        self.db.flush()

        # -------------------------------------------------
        # Commit complete transaction
        # -------------------------------------------------

        self.db.commit()

        self.db.refresh(institute)
        self.db.refresh(admin_user)

        # -------------------------------------------------
        # Return Institute + Admin
        # -------------------------------------------------

        return {
            "id": institute.id,
            "name": institute.name,
            "code": institute.code,
            "email": institute.email,
            "phone": institute.phone,
            "address": institute.address,
            "logo_url": institute.logo_url,
            "country_code": institute.country_code,
            "timezone": institute.timezone,
            "is_active": institute.is_active,
            "admin": {
                "id": admin_user.id,
                "full_name": admin_user.full_name,
                "email": admin_user.email,
                "phone": admin_user.phone,
                "institute_id": admin_user.institute_id,
                "branch_id": admin_user.branch_id,
                "is_active": admin_user.is_active,
                "is_verified": admin_user.is_verified,
            },
        }

    def get_institute(
        self,
        institute_id: int,
    ) -> dict:
        """
        Get an institute by ID with its
        Institute Admin details.
        """

        institute = self.repository.get_by_id(
            institute_id
        )

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        return self._build_institute_response(
            institute
        )

    def get_all_institutes(
        self,
    ) -> list[dict]:
        """
        Get all institutes with their
        Institute Admin details.
        """

        institutes = self.repository.get_all()

        return [
            self._build_institute_response(
                institute
            )
            for institute in institutes
        ]

    def update_institute(
        self,
        institute_id: int,
        data: InstituteUpdate,
    ) -> dict:
        """
        Update an existing institute and return
        the updated institute with its admin details.
        """

        institute = self.repository.get_by_id(
            institute_id
        )

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # -------------------------------------------------
        # Normalize and validate email
        # -------------------------------------------------

        if "email" in update_data:

            if update_data["email"]:

                new_email = (
                    update_data["email"]
                    .lower()
                    .strip()
                )

                existing_email = (
                    self.repository.get_by_email(
                        new_email
                    )
                )

                if (
                    existing_email
                    and existing_email.id != institute.id
                ):
                    raise AppException(
                        message="An institute with this email already exists.",
                        status_code=409,
                        code="INSTITUTE_EMAIL_ALREADY_EXISTS",
                    )

                update_data["email"] = new_email

            else:
                update_data["email"] = None

        # -------------------------------------------------
        # Normalize string fields
        # -------------------------------------------------

        string_fields = [
            "name",
            "phone",
            "address",
            "logo_url",
            "timezone",
        ]

        for field in string_fields:

            if field in update_data:

                value = update_data[field]

                if value is not None:
                    update_data[field] = value.strip()

        # -------------------------------------------------
        # Normalize country code
        # -------------------------------------------------

        if "country_code" in update_data:

            if update_data["country_code"]:
                update_data["country_code"] = (
                    update_data["country_code"].upper()
                )

        # -------------------------------------------------
        # Apply update
        # -------------------------------------------------

        for field, value in update_data.items():

            setattr(
                institute,
                field,
                value,
            )

        institute = self.repository.update(
            institute
        )

        self.db.commit()
        self.db.refresh(institute)

        return self._build_institute_response(
            institute
        )

    def delete_institute(
        self,
        institute_id: int,
    ) -> None:
        """
        Delete an institute.
        """

        institute = self.repository.get_by_id(
            institute_id
        )

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        self.repository.delete(institute)

        self.db.commit()