from pathlib import Path
from dotenv import load_dotenv
import os
import sys

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import ValidationError

# Load environment variables from the .env file at the project root.
load_dotenv()

# Resolve the backend directory so the .env file can be loaded reliably.
BACKEND_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_name: str = Field(default=os.getenv("APP_NAME"))
    app_version: str = Field(default=os.getenv("APP_VERSION"))
    app_env: str = Field(default=os.getenv("APP_ENV"))
    database_name: str = Field(default=os.getenv("DATABASE_NAME"))

    # Comma-separated origins are supported automatically by pydantic-settings
    # when provided as a JSON-like list or can be normalized manually if needed.
    backend_cors_origins: str = Field(default=os.getenv("BACKEND_CORS_ORIGINS"))

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Return normalized CORS origins as a clean list."""
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

try:
    settings = Settings()
except ValidationError:
    # If this error occurs, most likely is due to env variables
    print("Error loading settings. Please check your .env file and environment variables.")
    sys.exit(1)
