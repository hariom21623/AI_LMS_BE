from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InstituteAdminCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)


class InstituteCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    code: str = Field(..., min_length=2, max_length=50)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = None
    logo_url: str | None = Field(default=None, max_length=500)
    country_code: str = Field(default="IN", min_length=2, max_length=2)
    timezone: str = Field(default="Asia/Kolkata", max_length=100)

    admin: InstituteAdminCreate


class InstituteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = None
    logo_url: str | None = Field(default=None, max_length=500)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    timezone: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class InstituteAdminResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    institute_id: int
    branch_id: int | None
    is_active: bool
    is_verified: bool


class InstituteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

    admin: InstituteAdminResponse | None = None


class InstituteCreateResponse(BaseModel):
    """
    Response returned when Super Admin creates
    an institute together with its initial admin.
    """

    model_config = ConfigDict(from_attributes=True)

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

    admin: InstituteAdminResponse | None = None