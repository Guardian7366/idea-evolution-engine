from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Resolve the backend directory so the .env file can be loaded reliably.
BACKEND_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_name: str = Field(default="Idea Evolution Engine API")
    app_version: str = Field(default="0.1.0")
    app_env: str = Field(default="development")

    # Comma-separated origins are supported automatically by pydantic-settings
    # when provided as a JSON-like list or can be normalized manually if needed.
    backend_cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
    )

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


settings = Settings()