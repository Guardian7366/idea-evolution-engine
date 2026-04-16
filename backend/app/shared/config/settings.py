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

    app_name: str = Field(default=os.getenv("APP_NAME", "Idea Evolution Engine API"))
    app_version: str = Field(default=os.getenv("APP_VERSION", "0.1.0"))
    app_env: str = Field(default=os.getenv("APP_ENV", "development"))
    database_name: str = Field(default=os.getenv("DATABASE_NAME", "idea_evolution.db"))

    # Comma-separated origins are supported automatically by pydantic-settings
    # when provided as a JSON-like list or can be normalized manually if needed.
    backend_cors_origins: str = Field(default=os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"))

    # Ollama LLM configuration
    ollama_base_url: str = Field(default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    ollama_model: str = Field(default=os.getenv("OLLAMA_MODEL", "qwen2.5"))

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
