from fastapi import FastAPI

from app.core.config import settings
from app.db.health import check_database_connection


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
)


@app.get("/api/v1/health")
def health_check():
    database_connected = check_database_connection()

    return {
        "success": True,
        "environment": settings.APP_ENV,
        "api": "healthy",
        "database": "connected" if database_connected else "disconnected",
    }