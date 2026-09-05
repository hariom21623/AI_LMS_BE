from sqlalchemy.orm import Session

from app.models.course import Course


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, course_id: int) -> Course | None:
        return (
            self.db.query(Course)
            .filter(Course.id == course_id)
            .first()
        )

    def get_by_code(
        self,
        institute_id: int,
        branch_id: int,
        code: str,
    ) -> Course | None:
        return (
            self.db.query(Course)
            .filter(
                Course.institute_id == institute_id,
                Course.branch_id == branch_id,
                Course.code == code,
            )
            .first()
        )

    def get_by_branch(
        self,
        institute_id: int,
        branch_id: int,
    ) -> list[Course]:
        return (
            self.db.query(Course)
            .filter(
                Course.institute_id == institute_id,
                Course.branch_id == branch_id,
            )
            .order_by(Course.id.desc())
            .all()
        )

    def create(self, course: Course) -> Course:
        self.db.add(course)
        self.db.flush()
        self.db.refresh(course)
        return course

    def update(self, course: Course) -> Course:
        self.db.flush()
        self.db.refresh(course)
        return course

    def delete(self, course: Course) -> None:
        self.db.delete(course)
        self.db.flush()