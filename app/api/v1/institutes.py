from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.institute import (
    InstituteCreate,
    InstituteCreateResponse,
    InstituteResponse,
    InstituteUpdate,
)
from app.services.institute_service import InstituteService


router = APIRouter(
    prefix="/institutes",
    tags=["Institutes"],
)


@router.post(
    "",
    response_model=InstituteCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_institute(
    data: InstituteCreate,
    current_user: User = Depends(
        require_permission("institute:create")
    ),
    db: Session = Depends(get_db),
):
    service = InstituteService(db)

    return service.create_institute(data)


@router.get(
    "",
    response_model=list[InstituteResponse],
)
def get_all_institutes(
    current_user: User = Depends(
        require_permission("institute:read")
    ),
    db: Session = Depends(get_db),
):
    service = InstituteService(db)

    return service.get_all_institutes()


@router.get(
    "/{institute_id}",
    response_model=InstituteResponse,
)
def get_institute(
    institute_id: int,
    current_user: User = Depends(
        require_permission("institute:read")
    ),
    db: Session = Depends(get_db),
):
    service = InstituteService(db)

    return service.get_institute(institute_id)


@router.put(
    "/{institute_id}",
    response_model=InstituteResponse,
)
def update_institute(
    institute_id: int,
    data: InstituteUpdate,
    current_user: User = Depends(
        require_permission("institute:update")
    ),
    db: Session = Depends(get_db),
):
    service = InstituteService(db)

    return service.update_institute(
        institute_id=institute_id,
        data=data,
    )


@router.delete(
    "/{institute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_institute(
    institute_id: int,
    current_user: User = Depends(
        require_permission("institute:delete")
    ),
    db: Session = Depends(get_db),
):
    service = InstituteService(db)

    service.delete_institute(institute_id)

    return None