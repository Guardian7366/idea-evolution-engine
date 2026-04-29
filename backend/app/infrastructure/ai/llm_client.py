"""
llm_client.py — HTTP client for communicating with the local Ollama runtime.

Reads OLLAMA_BASE_URL, OLLAMA_MODEL, and OLLAMA_TIMEOUT from settings.py.
Uses Python's built-in urllib + anyio.to_thread.run_sync for async-compatible
HTTP without adding dependencies beyond what FastAPI already requires.

Error hierarchy (all inherit RuntimeError so existing callers still work):
  OllamaUnavailableError — Ollama process not running / refused connection.
  OllamaTimeoutError     — Request exceeded the configured timeout.
  OllamaHTTPError        — Ollama returned a non-2xx HTTP status.
  OllamaResponseError    — Ollama responded but the payload was unexpected.
"""

import json
import logging
import socket
import urllib.error
import urllib.request

import anyio

from app.shared.config import settings

logger = logging.getLogger(__name__)


# ── Public exception types ────────────────────────────────────────────────────

class OllamaUnavailableError(RuntimeError):
    """Raised when Ollama is not reachable (not running or wrong URL)."""


class OllamaTimeoutError(RuntimeError):
    """Raised when the model takes longer than ollama_timeout seconds."""


class OllamaHTTPError(RuntimeError):
    """Raised when Ollama returns a non-2xx HTTP status."""
    def __init__(self, code: int, body: str) -> None:
        super().__init__(f"Ollama HTTP {code}: {body}")
        self.code = code
        self.body = body


class OllamaResponseError(RuntimeError):
    """Raised when Ollama responds but the payload is missing expected fields."""


# ── Client ────────────────────────────────────────────────────────────────────

class LLMClient:
    """Async wrapper around Ollama's /api/chat endpoint using stdlib urllib."""

    def __init__(self) -> None:
        self._base_url: str = settings.ollama_base_url
        self._model: str = settings.ollama_model
        self._timeout: float = settings.ollama_timeout
        logger.info(
            "[LLMClient] Initialised — model=%s  url=%s  timeout=%ss",
            self._model, self._base_url, self._timeout,
        )

    async def chat(self, system: str, user: str) -> str:
        """
        Send a system + user message to Ollama and return the response text.

        Forces JSON output mode via ``format: "json"``.
        Runs the blocking urllib call in a thread via anyio so the event loop
        is never blocked.

        Raises:
            OllamaUnavailableError  — if Ollama is not reachable.
            OllamaTimeoutError      — if the request exceeds the timeout.
            OllamaHTTPError         — if Ollama returns a non-2xx status.
            OllamaResponseError     — if the response body is malformed.
        """
        payload = json.dumps({
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            "stream": False,
            "format": "json",
        }).encode("utf-8")

        url = f"{self._base_url}/api/chat"

        def _sync_request() -> str:
            req = urllib.request.Request(
                url=url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read().decode("utf-8")

                try:
                    data = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise OllamaResponseError(
                        f"Ollama returned non-JSON body: {raw[:200]!r}"
                    ) from exc

                try:
                    return data["message"]["content"]
                except (KeyError, TypeError) as exc:
                    raise OllamaResponseError(
                        f"Ollama response missing 'message.content'. "
                        f"Keys present: {list(data.keys())}"
                    ) from exc

            except (TimeoutError, socket.timeout) as exc:
                raise OllamaTimeoutError(
                    f"Request to {url} timed out after {self._timeout}s. "
                    "Consider increasing OLLAMA_TIMEOUT in your .env."
                ) from exc

            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                raise OllamaHTTPError(exc.code, body) from exc

            except urllib.error.URLError as exc:
                # URLError wraps socket errors including connection refused.
                reason = str(exc.reason)
                if "refused" in reason.lower() or "connect" in reason.lower():
                    raise OllamaUnavailableError(
                        f"Cannot reach Ollama at {url}. "
                        "Make sure Ollama is running (ollama serve)."
                    ) from exc
                raise OllamaUnavailableError(
                    f"Network error reaching Ollama at {url}: {reason}"
                ) from exc

        return await anyio.to_thread.run_sync(_sync_request)


# ── Module-level singleton ────────────────────────────────────────────────────

_llm_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    """Return the shared LLMClient instance (lazy init)."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
