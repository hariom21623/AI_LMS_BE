from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    institute_id: int = Field(..., gt=0)
    branch_id: int = Field(..., gt=0)

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

    description: str | None = None


class CourseUpdate(BaseModel):
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

    description: str | None = None

    is_active: bool | None = None


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institute_id: int
    branch_id: int
    name: str
    code: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime