from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.branches import router as branch_router
from app.api.v1.branch_transfer import router as branch_transfer_router
from app.api.v1.institutes import router as institute_router
from app.api.v1.user_management import (
    router as user_management_router,
)
from app.api.v1.user_roles import router as user_role_router
from app.api.v1.branch_transfer_reversal import (
    router as branch_transfer_reversal_router,
)
from app.api.v1.course import router as course_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(institute_router)
api_router.include_router(user_role_router)
api_router.include_router(branch_router)
api_router.include_router(user_management_router)
api_router.include_router(branch_transfer_router)
api_router.include_router(branch_transfer_reversal_router)
api_router.include_router(course_router)