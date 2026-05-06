from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.domain.value_objects.transformation_type import TransformationType


class MockAIProvider:
    def generate_variants(self, idea_text: str, language: str = "en") -> list[dict]:
        now = datetime.now(timezone.utc)

        if language == "es":
            return [
                {
                    "id": f"var_{uuid4().hex}",
                    "title": "Enfoque práctico",
                    "description": "Una versión orientada a implementación concreta y utilidad inmediata.",
                    "order_index": 1,
                    "created_at": now,
                },
                {
                    "id": f"var_{uuid4().hex}",
                    "title": "Enfoque innovador",
                    "description": "Una versión orientada a diferenciación, creatividad y propuesta novedosa.",
                    "order_index": 2,
                    "created_at": now,
                },
                {
                    "id": f"var_{uuid4().hex}",
                    "title": "Enfoque de negocio",
                    "description": "Una versión orientada a valor de mercado, usuarios y monetización.",
                    "order_index": 3,
                    "created_at": now,
                },
            ]

        return [
            {
                "id": f"var_{uuid4().hex}",
                "title": "Practical approach",
                "description": "A version focused on concrete implementation and immediate usefulness.",
                "order_index": 1,
                "created_at": now,
            },
            {
                "id": f"var_{uuid4().hex}",
                "title": "Innovative approach",
                "description": "A version focused on differentiation, creativity, and novelty.",
                "order_index": 2,
                "created_at": now,
            },
            {
                "id": f"var_{uuid4().hex}",
                "title": "Business approach",
                "description": "A version focused on market value, users, and monetization.",
                "order_index": 3,
                "created_at": now,
            },
        ]

    def transform_version(
        self,
        *,
        parent_content: str,
        transformation_type: TransformationType,
        instruction: str | None,
        language: str = "en",
    ) -> dict:
        now = datetime.now(timezone.utc)

        if language == "es":
            if transformation_type == TransformationType.EVOLUTION:
                content = (
                    f"{parent_content}\n\n"
                    "Evolución aplicada: esta nueva versión amplía la idea previa, "
                    "agrega más detalle, mejora estructura y profundiza el concepto."
                )
            elif transformation_type == TransformationType.REFINEMENT:
                content = (
                    f"{parent_content}\n\n"
                    f"Refinamiento aplicado según instrucción del usuario: {instruction}. "
                    "La versión fue ajustada para seguir esa dirección de manera más clara."
                )
            elif transformation_type == TransformationType.MUTATION:
                content = (
                    f"{parent_content}\n\n"
                    "Mutación creativa aplicada: esta nueva versión explora un camino más "
                    "arriesgado, diferente o menos conservador respecto a la versión anterior."
                )
            else:
                raise ValueError("Unsupported transformation type for mock provider.")
        else:
            if transformation_type == TransformationType.EVOLUTION:
                content = (
                    f"{parent_content}\n\n"
                    "Evolution applied: this new version expands the previous idea, "
                    "adds more detail, improves structure, and deepens the concept."
                )
            elif transformation_type == TransformationType.REFINEMENT:
                content = (
                    f"{parent_content}\n\n"
                    f"Refinement applied according to user instruction: {instruction}. "
                    "The version was adjusted to follow that direction more clearly."
                )
            elif transformation_type == TransformationType.MUTATION:
                content = (
                    f"{parent_content}\n\n"
                    "Creative mutation applied: this new version explores a more risky, "
                    "different, or less conservative path than the previous version."
                )
            else:
                raise ValueError("Unsupported transformation type for mock provider.")

        return {
            "id": f"ver_{uuid4().hex}",
            "content": content,
            "created_at": now,
            "updated_at": now,
        }

    def analyze_perspective(
        self,
        *,
        version_id: str,
        perspective: str,
        language: str = "en",
    ) -> dict:
        now = datetime.now(timezone.utc)

        if language == "es":
            content = f"Análisis generado para la perspectiva '{perspective}'."
        else:
            content = f"Analysis generated for perspective '{perspective}'."

        return {
            "id": f"ana_{uuid4().hex}",
            "analysis_type": perspective,
            "content": content,
            "created_at": now,
        }

    def generate_synthesis(
        self,
        *,
        idea_id: str,
        version_id: str,
        language: str = "en",
    ) -> dict:
        now = datetime.now(timezone.utc)

        if language == "es":
            return {
                "id": f"syn_{uuid4().hex}",
                "summary": "Resumen generado para la idea evolucionada.",
                "value_proposition": "Propuesta de valor generada para la idea.",
                "target_audience": "Usuarios objetivo definidos para esta versión.",
                "structured_description": "Descripción estructurada del concepto final.",
                "next_steps": "Siguientes pasos sugeridos para continuar el desarrollo.",
                "created_at": now,
            }

        return {
            "id": f"syn_{uuid4().hex}",
            "summary": "Summary generated for the evolved idea.",
            "value_proposition": "Value proposition generated for the idea.",
            "target_audience": "Target users defined for this version.",
            "structured_description": "Structured description of the final concept.",
            "next_steps": "Suggested next steps to continue development.",
            "created_at": now,
        }

    def compare_versions(
        self,
        *,
        left_version_content: str,
        right_version_content: str,
        language: str = "en",
    ) -> dict:
        now = datetime.now(timezone.utc)

        if language == "es":
            comparison_text = (
                "La versión derecha amplía o modifica elementos respecto a la izquierda. "
                "En general, la comparación sugiere una evolución del concepto con cambios "
                "en claridad, enfoque o nivel de desarrollo."
            )
        else:
            comparison_text = (
                "The right version expands or modifies elements compared to the left one. "
                "Overall, the comparison suggests an evolution of the concept with changes "
                "in clarity, focus, or level of development."
            )

        return {
            "id": f"cmp_{uuid4().hex}",
            "comparison_text": comparison_text,
            "created_at": now,
        }