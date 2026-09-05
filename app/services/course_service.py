from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.course import Course
from app.repositories.course_repository import CourseRepository


class CourseService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CourseRepository(db)

    def create_course(
        self,
        institute_id: int,
        branch_id: int,
        name: str,
        code: str,
        description: str | None,
    ) -> Course:
        existing_course = self.repository.get_by_code(
            institute_id=institute_id,
            branch_id=branch_id,
            code=code,
        )

        if existing_course:
            raise AppException(
                "A course with this code already exists in this branch.",
                409,
                "COURSE_CODE_ALREADY_EXISTS",
            )

        course = Course(
            institute_id=institute_id,
            branch_id=branch_id,
            name=name,
            code=code,
            description=description,
        )

        try:
            self.repository.create(course)
            self.db.commit()
            self.db.refresh(course)
            return course

        except IntegrityError:
            self.db.rollback()
            raise AppException(
                "Unable to create course.",
                409,
                "COURSE_CREATE_FAILED",
            )

        except Exception:
            self.db.rollback()
            raise

    def get_course(self, course_id: int) -> Course:
        course = self.repository.get_by_id(course_id)

        if not course:
            raise AppException(
                "Course not found.",
                404,
                "COURSE_NOT_FOUND",
            )

        return course

    def list_courses(
        self,
        institute_id: int,
        branch_id: int,
    ) -> list[Course]:
        return self.repository.get_by_branch(
            institute_id=institute_id,
            branch_id=branch_id,
        )

    def update_course(
        self,
        course_id: int,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Course:
        course = self.get_course(course_id)

        if code is not None and code != course.code:
            existing_course = self.repository.get_by_code(
                institute_id=course.institute_id,
                branch_id=course.branch_id,
                code=code,
            )

            if existing_course and existing_course.id != course.id:
                raise AppException(
                    "A course with this code already exists in this branch.",
                    409,
                    "COURSE_CODE_ALREADY_EXISTS",
                )

            course.code = code

        if name is not None:
            course.name = name

        if description is not None:
            course.description = description

        if is_active is not None:
            course.is_active = is_active

        try:
            self.repository.update(course)
            self.db.commit()
            self.db.refresh(course)
            return course

        except IntegrityError:
            self.db.rollback()
            raise AppException(
                "Unable to update course.",
                409,
                "COURSE_UPDATE_FAILED",
            )

        except Exception:
            self.db.rollback()
            raise

    def delete_course(self, course_id: int) -> None:
        course = self.get_course(course_id)

        try:
            self.repository.delete(course)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise