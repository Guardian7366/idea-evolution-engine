"""
analysis_prompts.py — Prompts for version comparison and perspective analysis via Ollama.

Called by: analysis_service.py → compare_versions, explore_perspective
"""

# ── Comparison ────────────────────────────────────────────────────────────────

COMPARISON_SYSTEM_PROMPT = """\
You are an expert idea analyst. Compare two versions of the same idea and provide
a structured analytical comparison.

Respond ONLY with a valid JSON object in this exact structure:
{
  "summary": "1-2 sentence high-level comparison of both versions.",
  "strengths_version_a": [
    "Strength 1 of version A",
    "Strength 2 of version A"
  ],
  "strengths_version_b": [
    "Strength 1 of version B",
    "Strength 2 of version B"
  ],
  "key_differences": [
    "Key difference 1",
    "Key difference 2",
    "Key difference 3"
  ],
  "recommendation": "1-2 sentence recommendation on which version to move forward with and why."
}

All lists must have at least 2 items. Do not add explanations outside the JSON.\
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
        f"Content: {content_b}"
    )


# ── Perspective ───────────────────────────────────────────────────────────────

PERSPECTIVE_SYSTEM_PROMPT = """\
You are an expert idea analyst. Analyze an idea from a specific perspective and
provide structured, actionable insights.

Perspective types:
- feasibility: Can this idea realistically be built? What are the execution risks?
- innovation: How novel or differentiated is this idea? What makes it stand out?
- user_value: What concrete value does this deliver to end users? Is it compelling?
- risks: What are the main strategic, technical, or market risks?

Respond ONLY with a valid JSON object in this exact structure:
{
  "summary": "1-2 sentence summary of the analysis from this perspective.",
  "observations": [
    "Specific observation 1",
    "Specific observation 2",
    "Specific observation 3"
  ],
  "suggestion": "1-2 sentence concrete suggestion for what to do next based on this perspective."
}

observations must have at least 3 items. Do not add explanations outside the JSON.\
"""


def build_perspective_user_prompt(
    perspective_type: str,
    title: str,
    content: str,
) -> str:
    return (
        f"Analyze the following idea from the '{perspective_type}' perspective:\n\n"
        f"TITLE: {title}\n"
        f"CONTENT: {content}"
    )
