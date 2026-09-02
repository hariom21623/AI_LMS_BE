import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


def get_env_file() -> str:
    environment = os.getenv("APP_ENV", "local").lower()

    env_files = {
        "local": ".env.local",
        "dev": ".env.dev",
        "prod": ".env.prod",
    }

    if environment not in env_files:
        raise ValueError(
            f"Invalid APP_ENV='{environment}'. "
            f"Allowed values: local, dev, prod"
        )

    return env_files[environment]


class Settings(BaseSettings):

    APP_NAME: str = "AI-LMS"
    APP_ENV: str = "local"
    DEBUG: bool = True

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_REFRESH_SECRET: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    FRONTEND_URL: str
    CORS_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / get_env_file(),
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()