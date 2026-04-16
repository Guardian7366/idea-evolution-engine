"""
synthesis_prompts.py — Prompts for generating the final idea synthesis via Ollama.

Called by: synthesis_service.py → generate_final_synthesis
"""

SYNTHESIS_SYSTEM_PROMPT = """\
You are an expert product strategist. Your task is to generate a final structured synthesis
of an idea that has evolved through multiple iterations.

The synthesis must capture the essence of the idea in its most refined state and provide
clear, actionable guidance for what to do next.

Respond ONLY with a valid JSON object in this exact structure:
{
  "title": "Final synthesized title for the idea (max 80 chars)",
  "core_concept": "2-3 sentence summary of the core concept in its final form.",
  "value_proposition": "2-3 sentence description of the main value this idea delivers to users.",
  "recommended_next_step": "1-2 sentence concrete recommendation for the most important next action.",
  "notes": [
    "Important consideration or insight 1",
    "Important consideration or insight 2",
    "Important consideration or insight 3"
  ]
}

notes must have at least 3 items. Do not add explanations outside the JSON.\
"""


def build_synthesis_user_prompt(
    original_prompt: str,
    final_title: str,
    final_content: str,
    total_versions: int,
) -> str:
    return (
        f"Generate a final synthesis for the following evolved idea:\n\n"
        f"ORIGINAL IDEA: {original_prompt}\n\n"
        f"FINAL VERSION TITLE: {final_title}\n"
        f"FINAL VERSION CONTENT: {final_content}\n\n"
        f"This idea went through {total_versions} version(s) before reaching this state."
    )
