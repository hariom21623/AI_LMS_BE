from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BranchTransferRequest(BaseModel):
    to_institute_id: int = Field(..., gt=0)
    reason: str | None = Field(default=None, max_length=500)


class BranchTransferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    branch_id: int | None
    from_institute_id: int | None
    to_institute_id: int | None
    reason: str | None
    transferred_by: int | None
    transferred_at: datetime
    is_reversed: bool
    reversed_at: datetime | None
    reversed_by: int | None