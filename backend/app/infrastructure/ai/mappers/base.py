import json
import re
from typing import Any


class LLMParseError(Exception):
    """Raised when the LLM response cannot be parsed into the expected structure."""


def extract_json(raw: str) -> dict[str, Any]:
    """
    Attempt to extract a JSON object from an LLM response string.

    Tries in order:
    1. Direct parse (Ollama format=json should produce clean JSON)
    2. Strip markdown code fences (```json ... ```)
    3. Extract first {...} block from the string
    """
    text = raw.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown fences
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        try:
            return json.loads(fence_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Extract first complete JSON object
    brace_match = re.search(r"\{[\s\S]*\}", text)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    raise LLMParseError(
        f"Could not parse JSON from LLM response. "
        f"First 200 chars: {raw[:200]!r}"
    )


def require_keys(data: dict[str, Any], keys: list[str], context: str) -> None:
    missing = [k for k in keys if k not in data]
    if missing:
        raise LLMParseError(
            f"LLM response for {context} is missing required keys: {missing}. "
            f"Got keys: {list(data.keys())}"
        )
