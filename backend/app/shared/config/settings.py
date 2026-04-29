from pathlib import Path
from dotenv import load_dotenv
import os
import sys
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import ValidationError

# Load environment variables from the .env file at the project root.
load_dotenv()

# Resolve the backend directory so the .env file can be loaded reliably.
BACKEND_DIR = Path(__file__).resolve().parents[4]

# ── Model profiles ────────────────────────────────────────────────────────────
# Each profile bundles a model name with its recommended timeout.
# Select a profile via MODEL_PROFILE env var.
# OLLAMA_MODEL and OLLAMA_TIMEOUT always override the profile values if set.

_MODEL_PROFILES: dict[str, dict[str, Any]] = {
    # Full-precision Llama 3.1 8B — best quality, requires ~17 GB VRAM (fits RX 7900 XT).
    "capable": {
        "model": "llama3.1:latest",
        "timeout": 180.0,
    },
    # Qwen 2.5 7B — lightweight, runs on CPU or low-VRAM GPUs (~5 GB VRAM at Q4).
    "fast": {
        "model": "qwen2.5",
        "timeout": 120.0,
    },
}

_VALID_PROFILES = set(_MODEL_PROFILES.keys())


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_name: str = Field(default=os.getenv("APP_NAME", "Idea Evolution Engine API"))
    app_version: str = Field(default=os.getenv("APP_VERSION", "0.1.0"))
    app_env: str = Field(default=os.getenv("APP_ENV", "development"))
    database_name: str = Field(default=os.getenv("DATABASE_NAME", "idea_evolution.db"))

    # Comma-separated origins supported automatically by pydantic-settings.
    backend_cors_origins: str = Field(
        default=os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    )

    # Ollama connection
    ollama_base_url: str = Field(default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

    # Active model profile. Must be one of _VALID_PROFILES.
    # Individual OLLAMA_MODEL / OLLAMA_TIMEOUT env vars take priority over the profile.
    model_profile: str = Field(default=os.getenv("MODEL_PROFILE", "capable"))

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    # ── Computed properties (profile + optional env override) ─────────────────

    @property
    def ollama_model(self) -> str:
        """Model name: OLLAMA_MODEL env var > profile default."""
        override = os.getenv("OLLAMA_MODEL")
        if override:
            return override
        profile = _MODEL_PROFILES.get(self.model_profile, _MODEL_PROFILES["capable"])
        return profile["model"]

    @property
    def ollama_timeout(self) -> float:
        """Request timeout in seconds: OLLAMA_TIMEOUT env var > profile default."""
        override = os.getenv("OLLAMA_TIMEOUT")
        if override:
            return float(override)
        profile = _MODEL_PROFILES.get(self.model_profile, _MODEL_PROFILES["capable"])
        return profile["timeout"]

    @property
    def cors_origins_list(self) -> list[str]:
        """Return normalized CORS origins as a clean list."""
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def active_profile(self) -> dict[str, Any]:
        """Return the full profile dict currently active."""
        return _MODEL_PROFILES.get(self.model_profile, _MODEL_PROFILES["capable"])


try:
    settings = Settings()
    if settings.model_profile not in _VALID_PROFILES:
        print(
            f"[settings] Unknown MODEL_PROFILE '{settings.model_profile}'. "
            f"Valid options: {sorted(_VALID_PROFILES)}. Falling back to 'capable'."
        )
except ValidationError:
    print("Error loading settings. Please check your .env file and environment variables.")
    sys.exit(1)
