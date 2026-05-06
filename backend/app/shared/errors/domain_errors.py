from __future__ import annotations

from app.shared.errors.base import AppError


class DomainError(AppError):
    """Base domain error."""


class SessionNotFoundError(DomainError):
    pass


class IdeaNotFoundError(DomainError):
    pass


class VariantNotFoundError(DomainError):
    pass


class VariantSelectionError(DomainError):
    pass


class VersionNotFoundDomainError(DomainError):
    pass


class InvalidTransformationDomainError(DomainError):
    pass