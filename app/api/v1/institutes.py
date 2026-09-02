from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.institute import Institute
from app.schemas.institute import (
    InstituteCreate,
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
    response_model=InstituteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_institute(
    data: InstituteCreate,
    current_user: Institute = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new institute.
    """

    service = InstituteService(db)

    return service.create_institute(data)


@router.get(
    "",
    response_model=list[InstituteResponse],
)
def get_all_institutes(
    current_user: Institute = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all institutes.
    """

    service = InstituteService(db)

    return service.get_all_institutes()


@router.get(
    "/{institute_id}",
    response_model=InstituteResponse,
)
def get_institute(
    institute_id: int,
    current_user: Institute = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get an institute by ID.
    """

    service = InstituteService(db)

    return service.get_institute(institute_id)


@router.put(
    "/{institute_id}",
    response_model=InstituteResponse,
)
def update_institute(
    institute_id: int,
    data: InstituteUpdate,
    current_user: Institute = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an institute.
    """

    service = InstituteService(db)

    return service.update_institute(
        institute_id,
        data,
    )


@router.delete(
    "/{institute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_institute(
    institute_id: int,
    current_user: Institute = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an institute.
    """

    service = InstituteService(db)

    service.delete_institute(institute_id)

    return None