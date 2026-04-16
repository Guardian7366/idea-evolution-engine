"""
transformation_prompts.py — Prompts for transforming an idea version via Ollama.

Called by: version_service.py → ai_transform
"""

TRANSFORMATION_SYSTEM_PROMPT = """\
You are an expert idea evolution assistant. Your task is to transform an existing idea
according to a specific transformation type and user instruction.

Transformation types:
- evolve: Expand the idea into a broader, more developed direction. Add depth and new possibilities.
- refine: Sharpen the core concept. Improve clarity, reduce ambiguity, make it more practical.
- mutate: Introduce a bold experimental twist. Change the direction significantly.

Respond ONLY with a valid JSON object in this exact structure:
{
  "title": "Short title for the transformed idea (max 80 chars)",
  "content": "Full description of the transformed idea (3-5 sentences). Must reflect the transformation type and user instruction."
}

Do not add explanations outside the JSON.\
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
        f"USER INSTRUCTION: {instruction}"
    )
