from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from app.shared.config import settings

_request_log: dict[str, deque[float]] = defaultdict(deque)


def get_client_key(request: Request) -> str:
    if request.client:
        return request.client.host

    return "unknown"


def enforce_rate_limit(request: Request) -> None:
    if not settings.rate_limit_enabled:
        return

    now = time.monotonic()
    client_key = get_client_key(request)
    window_start = now - settings.rate_limit_window_seconds

    timestamps = _request_log[client_key]

    while timestamps and timestamps[0] < window_start:
        timestamps.popleft()

    if len(timestamps) >= settings.rate_limit_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please slow down.",
        )

    timestamps.append(now)