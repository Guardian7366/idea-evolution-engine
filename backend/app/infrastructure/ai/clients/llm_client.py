from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.shared.errors.infrastructure_errors import OllamaConnectionError


@dataclass
class LLMClient:
    base_url: str
    timeout: float = 120.0

    def post_json(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

        try:
            timeout_config = httpx.Timeout(
                timeout=self.timeout,
                connect=10.0,
            )

            with httpx.Client(timeout=timeout_config) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as exc:
            raise OllamaConnectionError(
                f"Ollama returned HTTP {exc.response.status_code}."
            ) from exc

        except httpx.TimeoutException as exc:
            raise OllamaConnectionError(
                "Ollama request timed out."
            ) from exc

        except httpx.RequestError as exc:
            raise OllamaConnectionError(
                "Failed to communicate with Ollama."
            ) from exc

        except ValueError as exc:
            raise OllamaConnectionError(
                "Ollama returned an invalid JSON response."
            ) from exc

    def generate_text(
        self,
        *,
        model: str,
        prompt: str,
        system: str | None = None,
        options: dict | None = None,
    ) -> str:
        payload: dict = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        if options:
            payload["options"] = options

        data = self.post_json("/api/generate", payload)
        return str(data.get("response", "")).strip()