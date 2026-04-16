"""
transformation_mapper.py — Maps raw Ollama JSON output to transformation content.

Called by: ollama_provider.py → transform_version
Returns a dict with 'title' and 'content' keys used to build the IdeaVariant.
"""

import json


def map_transformation(raw_json: str, transformation_type: str, instruction: str) -> dict[str, str]:
    """
    Parse Ollama's JSON response and return {'title': ..., 'content': ...}.

    Falls back to a generic result if the response is malformed.
    """
    try:
        data = json.loads(raw_json)
        title = str(data.get("title", "")).strip()
        content = str(data.get("content", "")).strip()

        if title and content:
            return {"title": title[:80], "content": content}

    except (json.JSONDecodeError, AttributeError, TypeError):
        pass

    # Fallback: build a minimal result from the instruction itself
    type_labels = {
        "evolve": "Evolved",
        "refine": "Refined",
        "mutate": "Mutated",
    }
    prefix = type_labels.get(transformation_type, "Transformed")
    return {
        "title": f"{prefix} Version",
        "content": f"Transformation ({transformation_type}): {instruction.rstrip('. ')}.",
    }
