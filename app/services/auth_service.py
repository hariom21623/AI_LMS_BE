from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    """
    Business logic related to authentication.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(
        self,
        data: RegisterRequest,
    ) -> User:
        """
        Register a new user.

        Public registration creates an unassigned user.
        Institute, branch and role are assigned later
        through protected administration workflows.
        """

        # Check duplicate email
        existing_user = self.user_repository.get_by_email(
            data.email.lower().strip()
        )

        if existing_user:
            raise AppException(
                message="A user with this email already exists.",
                status_code=409,
                code="EMAIL_ALREADY_EXISTS",
            )

        # Check duplicate phone
        if data.phone:
            existing_phone = self.user_repository.get_by_phone(
                data.phone
            )

            if existing_phone:
                raise AppException(
                    message="A user with this phone number already exists.",
                    status_code=409,
                    code="PHONE_ALREADY_EXISTS",
                )

        # Create user
        user = User(
            institute_id=None,
            branch_id=None,
            full_name=data.full_name.strip(),
            email=data.email.lower().strip(),
            phone=data.phone,
            password_hash=hash_password(data.password),
            is_active=True,
            is_verified=False,
        )

        user = self.user_repository.create(user)

        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User:
        """
        Authenticate a user using email and password.
        """

        user = self.user_repository.get_by_email(
            email.lower().strip()
        )

        if not user:
            raise AppException(
                message="Invalid email or password.",
                status_code=401,
                code="INVALID_CREDENTIALS",
            )

        if not user.is_active:
            raise AppException(
                message="User account is inactive.",
                status_code=403,
                code="USER_INACTIVE",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise AppException(
                message="Invalid email or password.",
                status_code=401,
                code="INVALID_CREDENTIALS",
            )

        return user