from __future__ import annotations

from functools import lru_cache
from typing import Annotated, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    rate_limit_enabled: bool = Field(default=True, alias="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=120, ge=1, le=1000, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600, alias="RATE_LIMIT_WINDOW_SECONDS")

    app_name: str = Field(default="Idea Evolution Engine API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=False, alias="APP_DEBUG")
    app_host: str = Field(default="127.0.0.1", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    backend_cors_origins: Annotated[List[str], NoDecode] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"],
        alias="BACKEND_CORS_ORIGINS",
    )

    security_headers_enabled: bool = Field(
        default=True,
        alias="SECURITY_HEADERS_ENABLED",
    )

    trusted_hosts: Annotated[List[str], NoDecode] = Field(
        default=["127.0.0.1", "localhost"],
        alias="TRUSTED_HOSTS",
    )

    sqlite_path: str = Field(default="app.db", alias="SQLITE_PATH")

    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")

    ollama_model_default: str = Field(
        default="qwen2.5:3b",
        alias="OLLAMA_MODEL_DEFAULT",
    )
    ollama_model_es: str = Field(
        default="qwen2.5:3b-enforce-es",
        alias="OLLAMA_MODEL_ES",
    )
    ollama_model_en: str = Field(
        default="qwen2.5:3b-enforce-en",
        alias="OLLAMA_MODEL_EN",
    )

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return []

    @field_validator("trusted_hosts", mode="before")
    @classmethod
    def parse_trusted_hosts(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return []


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()