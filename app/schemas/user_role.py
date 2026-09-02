from pydantic import BaseModel, Field


class UserRoleAssignRequest(BaseModel):
    """
    Request schema for assigning a role to a user.
    """

    role_id: int = Field(
        ...,
        gt=0,
    )


class UserSummary(BaseModel):
    """
    Basic user information returned with a role assignment.
    """

    id: int
    full_name: str
    email: str


class RoleSummary(BaseModel):
    """
    Basic role information returned with a role assignment.
    """

    id: int
    name: str
    code: str


class UserRoleResponse(BaseModel):
    """
    User-role assignment response.

    Includes both database IDs and human-readable
    user and role details for frontend use.
    """

    id: int

    user: UserSummary

    role: RoleSummary