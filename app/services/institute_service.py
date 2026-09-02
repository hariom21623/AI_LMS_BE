from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.institute import Institute
from app.repositories.institute_repository import InstituteRepository
from app.schemas.institute import (
    InstituteCreate,
    InstituteUpdate,
)


class InstituteService:
    """
    Business logic related to Institute.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = InstituteRepository(db)

    def create_institute(
        self,
        data: InstituteCreate,
    ) -> Institute:
        """
        Create a new institute.
        """

        code = data.code.strip().upper()

        existing_code = self.repository.get_by_code(code)

        if existing_code:
            raise AppException(
                message="An institute with this code already exists.",
                status_code=409,
                code="INSTITUTE_CODE_ALREADY_EXISTS",
            )

        if data.email:
            email = data.email.lower().strip()

            existing_email = self.repository.get_by_email(email)

            if existing_email:
                raise AppException(
                    message="An institute with this email already exists.",
                    status_code=409,
                    code="INSTITUTE_EMAIL_ALREADY_EXISTS",
                )
        else:
            email = None

        institute = Institute(
            name=data.name.strip(),
            code=code,
            email=email,
            phone=data.phone.strip() if data.phone else None,
            address=data.address.strip() if data.address else None,
            logo_url=data.logo_url.strip() if data.logo_url else None,
            country_code=data.country_code.upper(),
            timezone=data.timezone,
            is_active=True,
        )

        institute = self.repository.create(institute)

        self.db.commit()
        self.db.refresh(institute)

        return institute

    def get_institute(
        self,
        institute_id: int,
    ) -> Institute:
        """
        Get an institute by ID.
        """

        institute = self.repository.get_by_id(institute_id)

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        return institute

    def get_all_institutes(
        self,
    ) -> list[Institute]:
        """
        Get all institutes.
        """

        return self.repository.get_all()

    def update_institute(
        self,
        institute_id: int,
        data: InstituteUpdate,
    ) -> Institute:
        """
        Update an existing institute.
        """

        institute = self.repository.get_by_id(institute_id)

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "code" in update_data:
            new_code = update_data["code"].strip().upper()

            existing_code = self.repository.get_by_code(
                new_code
            )

            if (
                existing_code
                and existing_code.id != institute.id
            ):
                raise AppException(
                    message="An institute with this code already exists.",
                    status_code=409,
                    code="INSTITUTE_CODE_ALREADY_EXISTS",
                )

            update_data["code"] = new_code

        if "email" in update_data:
            if update_data["email"]:
                new_email = update_data["email"].lower().strip()

                existing_email = self.repository.get_by_email(
                    new_email
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

        if "country_code" in update_data:
            if update_data["country_code"]:
                update_data["country_code"] = (
                    update_data["country_code"].upper()
                )

        for field, value in update_data.items():
            setattr(
                institute,
                field,
                value,
            )

        institute = self.repository.update(institute)

        self.db.commit()
        self.db.refresh(institute)

        return institute

    def delete_institute(
        self,
        institute_id: int,
    ) -> None:
        """
        Delete an institute.
        """

        institute = self.repository.get_by_id(institute_id)

        if not institute:
            raise AppException(
                message="Institute not found.",
                status_code=404,
                code="INSTITUTE_NOT_FOUND",
            )

        self.repository.delete(institute)

        self.db.commit()