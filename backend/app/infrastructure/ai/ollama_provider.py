"""
ollama_provider.py — The real AI provider. Uses Qwen2.5 via Ollama.

This is the single point of contact between domain/application logic and the LLM.
It is called by four services:
  - idea_service.py      → generate_variants
  - version_service.py   → ai_transform
  - analysis_service.py  → compare_versions, explore_perspective
  - synthesis_service.py → generate_synthesis

Each method builds the correct prompt, calls LLMClient.chat(), and passes
the raw response through the corresponding mapper.
"""

import logging

logger = logging.getLogger(__name__)

from app.application.dto.comparison_dto import VersionComparisonResult
from app.application.dto.perspective_dto import PerspectiveAnalysisResult
from app.application.dto.synthesis_dto import FinalSynthesisResult
from app.application.dto.variant_dto import IdeaVariantItem
from app.infrastructure.ai.llm_client import LLMClient
from app.infrastructure.ai.mappers.analysis_mapper import map_comparison, map_perspective
from app.infrastructure.ai.mappers.synthesis_mapper import map_synthesis
from app.infrastructure.ai.mappers.transformation_mapper import map_transformation
from app.infrastructure.ai.mappers.variant_mapper import map_variants
from app.infrastructure.ai.prompts.analysis_prompts import (
    COMPARISON_SYSTEM_PROMPT,
    PERSPECTIVE_SYSTEM_PROMPT,
    build_comparison_user_prompt,
    build_perspective_user_prompt,
)
from app.infrastructure.ai.prompts.synthesis_prompts import (
    SYNTHESIS_SYSTEM_PROMPT,
    build_synthesis_user_prompt,
)
from app.infrastructure.ai.prompts.transformation_prompts import (
    TRANSFORMATION_SYSTEM_PROMPT,
    build_transformation_user_prompt,
)
from app.infrastructure.ai.prompts.variant_prompts import (
    VARIANT_SYSTEM_PROMPT,
    build_variant_user_prompt,
)


class OllamaProvider:
    """
    Facade over LLMClient that exposes one method per AI operation.
    Each method is responsible for: prompt → LLM call → mapper → typed result.
    """

    def __init__(self, client: LLMClient) -> None:
        self._client = client

    # ── idea_service ──────────────────────────────────────────────────────────

    async def generate_variants(self, initial_prompt: str) -> list[IdeaVariantItem]:
        """Generate 3 idea variants (expansion, focus, creative_twist)."""
        try:
            raw = await self._client.chat(
                system=VARIANT_SYSTEM_PROMPT,
                user=build_variant_user_prompt(initial_prompt),
            )
            return map_variants(raw)
        except Exception as e:
            logger.error(f"[OllamaProvider] Error generando variantes: {str(e)}")
            return map_variants("{}")

    # ── version_service ───────────────────────────────────────────────────────

    async def transform_version(
        self,
        current_title: str,
        current_content: str,
        transformation_type: str,
        instruction: str,
    ) -> dict[str, str]:
        """
        Transform an idea version. Returns {'title': ..., 'content': ...}
        ready to build an IdeaVariant.
        """
        try:
            raw = await self._client.chat(
                system=TRANSFORMATION_SYSTEM_PROMPT,
                user=build_transformation_user_prompt(
                    current_title=current_title,
                    current_content=current_content,
                    transformation_type=transformation_type,
                    instruction=instruction,
                ),
            )
            return map_transformation(raw, transformation_type, instruction)
        except Exception:
            return map_transformation("{}", transformation_type, instruction)

    # ── analysis_service ──────────────────────────────────────────────────────

    async def compare_versions(
        self,
        title_a: str,
        content_a: str,
        title_b: str,
        content_b: str,
    ) -> VersionComparisonResult:
        """Compare two idea versions and return structured analysis."""
        try:
            raw = await self._client.chat(
                system=COMPARISON_SYSTEM_PROMPT,
                user=build_comparison_user_prompt(title_a, content_a, title_b, content_b),
            )
            return map_comparison(raw)
        except Exception as e:
            logger.error(f"[OllamaProvider] Error comparando versiones: {str(e)}")
            return map_comparison("{}")

    async def explore_perspective(
        self,
        perspective_type: str,
        title: str,
        content: str,
    ) -> PerspectiveAnalysisResult:
        """Analyze an idea version from a specific perspective."""
        try:
            raw = await self._client.chat(
                system=PERSPECTIVE_SYSTEM_PROMPT,
                user=build_perspective_user_prompt(perspective_type, title, content),
            )
            return map_perspective(raw, perspective_type)
        except Exception as e:
            logger.error(f"[OllamaProvider] Error explorando perspectiva: {str(e)}")
            return map_perspective("{}", perspective_type)
        
    # ── synthesis_service ─────────────────────────────────────────────────────

    async def generate_synthesis(
        self,
        original_prompt: str,
        final_title: str,
        final_content: str,
        total_versions: int,
    ) -> FinalSynthesisResult:
        """Generate the final structured synthesis of an evolved idea."""
        try:
            raw = await self._client.chat(
                system=SYNTHESIS_SYSTEM_PROMPT,
                user=build_synthesis_user_prompt(
                    original_prompt=original_prompt,
                    final_title=final_title,
                    final_content=final_content,
                    total_versions=total_versions,
                ),
            )
            return map_synthesis(raw, total_versions)
        except Exception as e:
            logger.error(f"[OllamaProvider] Error generando síntesis: {str(e)}")
            return map_synthesis("{}", total_versions)