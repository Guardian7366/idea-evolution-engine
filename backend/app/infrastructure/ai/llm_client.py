"""
llm_client.py — HTTP client base for connecting to the local Ollama runtime.

Reads OLLAMA_BASE_URL and OLLAMA_MODEL from settings.py.
Uses Python's built-in urllib + anyio.to_thread.run_sync for async-compatible
HTTP without external dependencies beyond what FastAPI already requires.
"""

import json
import urllib.error
import urllib.request

import anyio

from app.shared.config import settings


class LLMClient:
    """Async wrapper around Ollama's /api/chat endpoint using stdlib urllib."""

    def __init__(self) -> None:
        self._base_url: str = settings.ollama_base_url
        self._model: str = settings.ollama_model
        self._timeout: float = 180.0

    async def chat(self, system: str, user: str) -> str:
        """
        Send a system + user message to Ollama and return the response text.

        Forces JSON output mode via `format: "json"`.
        Runs the blocking urllib call in a thread via anyio so it doesn't block
        the event loop.

        Raises RuntimeError on HTTP or connection errors.
        """
        payload = json.dumps({
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
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
                    data = json.loads(resp.read().decode("utf-8"))
                    return data["message"]["content"]
            except urllib.error.HTTPError as exc:
                raise RuntimeError(
                    f"Ollama HTTP error {exc.code}: {exc.read().decode('utf-8', errors='replace')}"
                ) from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(
                    f"Cannot reach Ollama at {url}: {exc.reason}"
                ) from exc

        return await anyio.to_thread.run_sync(_sync_request)


# Module-level singleton — instantiated once, reused across all requests.
_llm_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    """Return the shared LLMClient instance (lazy init)."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
