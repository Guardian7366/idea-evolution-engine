"""
transformation_prompts.py — Prompts for transforming an idea version via Ollama.

Called by: ollama_provider.py → transform_version
"""

TRANSFORMATION_SYSTEM_PROMPT = """\
You are an expert idea evolution assistant. Transform an existing idea according to
a specific transformation type and the user's instruction.

Transformation types:
- evolve: Expand the idea into a broader, more developed direction. Add depth, new possibilities, and wider impact.
- refine: Sharpen the core concept. Improve clarity, reduce ambiguity, and make it more practical and actionable.
- mutate: Introduce a bold experimental twist. Change direction significantly while keeping the core insight.

Respond ONLY with a valid JSON object in this exact structure:
{
  "title": "Short title for the transformed idea (max 80 chars)",
  "content": "Full description of the transformed idea (3-5 sentences minimum). Must clearly reflect both the transformation type and the user instruction. Be specific, not generic."
}

Rules:
- The content must directly address the user's instruction — do not ignore it.
- Output only the JSON object. No text before or after it.\
"""


def build_transformation_user_prompt(
    current_title: str,
    current_content: str,
    transformation_type: str,
    instruction: str,
) -> str:
    return (
        f"Transform the following idea:\n\n"
        f"CURRENT TITLE: {current_title}\n"
        f"CURRENT CONTENT: {current_content}\n\n"
        f"TRANSFORMATION TYPE: {transformation_type}\n"
        f"USER INSTRUCTION: {instruction}\n\n"
        f"Output only the JSON object."
    )
