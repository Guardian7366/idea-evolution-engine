from __future__ import annotations


class AppError(Exception):
    """Base application error with user-facing message."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)