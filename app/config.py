import os
from typing import Optional


class Settings:
    # Environment-based security
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    API_KEY: str = os.getenv("API_KEY", "demo-api-key-change-in-production")

    # Swagger UI control
    ENABLE_DOCS: bool = os.getenv("ENABLE_DOCS", "false").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

    # Security headers
    CORS_ORIGINS: list = ["https://your-domain.com"] if ENVIRONMENT == "production" else ["*"]


settings = Settings()
