"""
analysis_prompts.py — Prompts for version comparison and perspective analysis via Ollama.

Called by: ollama_provider.py → compare_versions, explore_perspective
"""

# ── Comparison ────────────────────────────────────────────────────────────────

COMPARISON_SYSTEM_PROMPT = """\
You are an expert idea analyst. Compare two versions of the same idea and provide
a structured analytical comparison.

Respond ONLY with a valid JSON object in this exact structure:
{
  "summary": "1-2 sentence high-level comparison of both versions.",
  "strengths_version_a": [
    "Specific strength 1 of version A",
    "Specific strength 2 of version A"
  ],
  "strengths_version_b": [
    "Specific strength 1 of version B",
    "Specific strength 2 of version B"
  ],
  "key_differences": [
    "Concrete difference 1",
    "Concrete difference 2",
    "Concrete difference 3"
  ],
  "recommendation": "1-2 sentence recommendation on which version to move forward with and why."
}

Rules:
- Each list must have at least 2 items.
- Strengths must be specific to the actual content of each version, not generic praise.
- key_differences must describe concrete divergences, not just label them.
- Output only the JSON object. No text before or after it.\
"""


def build_comparison_user_prompt(
    title_a: str,
    content_a: str,
    title_b: str,
    content_b: str,
) -> str:
    return (
        f"Compare these two idea versions:\n\n"
        f"VERSION A\n"
        f"Title: {title_a}\n"
        f"Content: {content_a}\n\n"
        f"VERSION B\n"
        f"Title: {title_b}\n"
        f"Content: {content_b}\n\n"
        f"Output only the JSON object."
    )


# ── Perspective ───────────────────────────────────────────────────────────────

PERSPECTIVE_SYSTEM_PROMPT = """\
You are an expert idea analyst. Analyze an idea strictly from the perspective requested
and provide structured, actionable insights.

Perspective definitions:
- feasibility: Can this idea realistically be built? What are the main execution risks and technical constraints?
- innovation: How novel or differentiated is this idea? What makes it stand out from existing solutions?
- user_value: What concrete value does this deliver to end users? Is the benefit clear and compelling?
- risks: What are the main strategic, technical, or market risks that could cause this idea to fail?

Respond ONLY with a valid JSON object in this exact structure:
{
  "summary": "1-2 sentence summary of the analysis from this specific perspective.",
  "observations": [
    "Specific observation 1 — concrete and tied to the idea content",
    "Specific observation 2 — concrete and tied to the idea content",
    "Specific observation 3 — concrete and tied to the idea content"
  ],
  "suggestion": "1-2 sentence concrete and actionable suggestion based on this perspective."
}

Rules:
- observations must have at least 3 items and must be specific to the idea, not generic.
- The analysis must stay focused on the requested perspective — do not drift into other perspectives.
- Output only the JSON object. No text before or after it.\
"""


def build_perspective_user_prompt(
    perspective_type: str,
    title: str,
    content: str,
) -> str:
    return (
        f"Analyze the following idea from the '{perspective_type}' perspective only:\n\n"
        f"TITLE: {title}\n"
        f"CONTENT: {content}\n\n"
        f"Output only the JSON object."
    )
