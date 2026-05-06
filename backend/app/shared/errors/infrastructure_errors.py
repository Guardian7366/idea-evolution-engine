from __future__ import annotations

from app.shared.errors.base import AppError


class InfrastructureError(AppError):
    """Base infrastructure error."""


class AIProviderConfigurationError(InfrastructureError):
    pass


class OllamaConnectionError(InfrastructureError):
    pass