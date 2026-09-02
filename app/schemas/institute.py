from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InstituteCreate(BaseModel):
    """
    Schema used when creating a new institute.
    """

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

    address: str | None = Field(
        default=None,
        max_length=1000,
    )

    logo_url: str | None = Field(
        default=None,
        max_length=500,
    )

    country_code: str = Field(
        default="IN",
        min_length=2,
        max_length=2,
    )

    timezone: str = Field(
        default="Asia/Kolkata",
        min_length=1,
        max_length=100,
    )


class InstituteUpdate(BaseModel):
    """
    Schema used when updating an existing institute.

    All fields are optional so that partial updates
    can be performed.
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

    address: str | None = Field(
        default=None,
        max_length=1000,
    )

    logo_url: str | None = Field(
        default=None,
        max_length=500,
    )

    country_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )

    timezone: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    is_active: bool | None = None


class InstituteResponse(BaseModel):
    """
    Schema used when returning institute data.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    code: str
    email: EmailStr | None
    phone: str | None
    address: str | None
    logo_url: str | None
    country_code: str
    timezone: str
    is_active: bool