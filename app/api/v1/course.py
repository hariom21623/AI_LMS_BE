from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.course_authorization import (
    require_course_create_access,
    require_course_delete_access,
    require_course_read_access,
    require_course_update_access,
)
from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.database import get_db
from app.models.user import User
from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
)
from app.services.course_service import CourseService


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_course_create_access(
        db=db,
        user=current_user,
        institute_id=payload.institute_id,
        branch_id=payload.branch_id,
    )

    service = CourseService(db)

    return service.create_course(
        institute_id=payload.institute_id,
        branch_id=payload.branch_id,
        name=payload.name,
        code=payload.code,
        description=payload.description,
    )


@router.get(
    "/branch/{branch_id}",
    response_model=list[CourseResponse],
)
def list_courses(
    branch_id: int,
    institute_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_course_read_access(
        db=db,
        user=current_user,
        institute_id=institute_id,
        branch_id=branch_id,
    )

    service = CourseService(db)

    return service.list_courses(
        institute_id=institute_id,
        branch_id=branch_id,
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CourseService(db)
    course = service.get_course(course_id)

    require_course_read_access(
        db=db,
        user=current_user,
        institute_id=course.institute_id,
        branch_id=course.branch_id,
    )

    return course


@router.put(
    "/{course_id}",
    response_model=CourseResponse,
)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CourseService(db)
    course = service.get_course(course_id)

    require_course_update_access(
        db=db,
        user=current_user,
        institute_id=course.institute_id,
        branch_id=course.branch_id,
    )

    return service.update_course(
        course_id=course_id,
        name=payload.name,
        code=payload.code,
        description=payload.description,
        is_active=payload.is_active,
    )


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CourseService(db)
    course = service.get_course(course_id)

    require_course_delete_access(
        db=db,
        user=current_user,
        institute_id=course.institute_id,
        branch_id=course.branch_id,
    )

    service.delete_course(course_id)

    return None