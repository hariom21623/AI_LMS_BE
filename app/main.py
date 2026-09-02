from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    database_exception_handler,
    global_exception_handler,
    validation_exception_handler,
)
from app.db.health import check_database_connection


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
)


# =========================================================
# Exception Handlers
# =========================================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# =========================================================
# API Routes
# =========================================================

app.include_router(
    api_router,
    prefix="/api/v1",
)


# =========================================================
# Health Check
# =========================================================

@app.get("/api/v1/health")
def health_check():
    database_connected = check_database_connection()

    return {
        "success": True,
        "environment": settings.APP_ENV,
        "api": "healthy",
        "database": (
            "connected"
            if database_connected
            else "disconnected"
        ),
    }