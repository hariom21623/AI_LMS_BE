from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BranchCreate(BaseModel):
    """
    Schema for creating a new branch.
    """

    institute_id: int = Field(
        ...,
        gt=0,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    address: str | None = None

    timezone: str = Field(
        default="Asia/Kolkata",
        max_length=100,
    )


class BranchUpdate(BaseModel):
    """
    Schema for updating an existing branch.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    address: str | None = None

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )

    is_active: bool | None = None


class BranchResponse(BaseModel):
    """
    Schema for branch response.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    institute_id: int
    name: str
    code: str
    email: EmailStr | None
    phone: str | None
    address: str | None
    timezone: str
    is_active: bool