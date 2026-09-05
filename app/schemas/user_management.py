from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    institute_id: int = Field(
        ...,
        gt=0,
    )

    branch_id: int | None = Field(
        default=None,
        gt=0,
    )

    role_id: int = Field(
        ...,
        gt=0,
    )

    timezone: str = Field(
        default="Asia/Kolkata",
        max_length=100,
    )


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    is_active: bool | None = None

    is_verified: bool | None = None

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )


class UserManagementResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    full_name: str
    email: EmailStr
    phone: str | None

    institute_id: int | None
    branch_id: int | None

    is_active: bool
    is_verified: bool

    timezone: str


class UserRoleAssignmentResponse(BaseModel):
    user_id: int
    role_id: int
    role_code: str
    role_name: str