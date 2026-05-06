from __future__ import annotations

from app.shared.errors.base import AppError


class PresentationError(AppError):
    """Base presentation/API error."""