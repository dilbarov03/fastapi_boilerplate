from pydantic_settings import BaseSettings
from typing import List
from zoneinfo import ZoneInfo


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Boilerplate"

    # Database
    # Default to Docker settings if env vars are missing
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:password123@localhost:5432/app_db"
    ASYNC_SQLALCHEMY_DATABASE_URI: str = "postgresql+asyncpg://postgres:password123@localhost:5432/app_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Admin
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Timezone
    DEFAULT_TIMEZONE: ZoneInfo = ZoneInfo("Asia/Tashkent")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
