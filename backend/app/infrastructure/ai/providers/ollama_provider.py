from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4
import logging
from app.domain.value_objects.transformation_type import TransformationType
from app.infrastructure.ai.clients.llm_client import LLMClient
from app.infrastructure.ai.prompts.analysis_prompts import build_perspective_analysis_prompt
from app.infrastructure.ai.prompts.comparison_prompts import build_comparison_prompt
from app.infrastructure.ai.prompts.synthesis_prompts import build_synthesis_prompt
from app.infrastructure.ai.prompts.transformation_prompts import build_transformation_prompt
from app.infrastructure.ai.prompts.variant_prompts import build_variant_generation_prompt
from app.infrastructure.ai.prompts.language_rewrite_prompts import build_language_rewrite_prompt
from app.shared.utils.language import detect_language
from app.infrastructure.ai.prompts.system_prompts import build_strict_system_prompt
logger = logging.getLogger(__name__)

class OllamaProvider:
    def __init__(
        self,
        client: LLMClient,
        default_model: str,
        spanish_model: str,
        english_model: str,
    ) -> None:
        self.client = client
        self.default_model = default_model
        self.spanish_model = spanish_model
        self.english_model = english_model

    def _clip_text(self, text: str, max_length: int = 8000) -> str:
        cleaned = text.strip()
        if len(cleaned) <= max_length:
            return cleaned
        return cleaned[:max_length].rstrip()
    
    def _resolve_model(self, language: str) -> str:
        if language == "es":
            return self.spanish_model
        if language == "en":
            return self.english_model
        return self.default_model
    
    def _system_prompt(self, language: str) -> str:
        return build_strict_system_prompt(language)
    
    def generate_variants(self, idea_text: str, language: str = "en") -> list[dict]:
        prompt = build_variant_generation_prompt(idea_text, language=language)

        model_name = self._resolve_model(language)

        logger.warning(
            "OLLAMA CALL -> method=%s language=%s model=%s",
            "generate_variants",  # cambia esto según el método
            language,
            model_name,
        )
        response_text = self.client.generate_text(
            model=model_name,
            prompt=prompt,
            system=self._system_prompt(language),
            options={
                "temperature": 0.1,
                "top_p": 0.2,
            },
        )
        response_text = self._enforce_output_language(response_text, language)
        response_text = self._clip_text(response_text)

        parsed = self._parse_variants_response(response_text)
        now = datetime.now(timezone.utc)

        results: list[dict] = []
        for index, item in enumerate(parsed[:3], start=1):
            results.append(
                {
                    "id": f"var_{uuid4().hex}",
                    "title": item["title"],
                    "description": item["description"],
                    "order_index": index,
                    "created_at": now,
                }
            )

        if len(results) < 3:
            fallback = self._fallback_variants(now, language=language)
            needed = 3 - len(results)
            results.extend(fallback[:needed])

        return results

    def transform_version(
        self,
        *,
        parent_content: str,
        transformation_type: TransformationType,
        instruction: str | None,
        language: str = "en",
    ) -> dict:
        normalized_parent_content = self._normalize_input_language(
            parent_content,
            language,
        )
        normalized_instruction = self._normalize_input_language(
            instruction,
            language,
        )

        prompt = build_transformation_prompt(
            parent_content=normalized_parent_content or parent_content,
            transformation_type=transformation_type.value,
            instruction=normalized_instruction,
            language=language,
        )

        model_name = self._resolve_model(language)
        logger.warning(
            "OLLAMA CALL -> method=%s language=%s model=%s",
            "transform_version",  # cambia esto según el método
            language,
            model_name,
        )
        
        response_text = self.client.generate_text(
            model=model_name,
            prompt=prompt,
            system=self._system_prompt(language),
            options={
                "temperature": 0.1,
                "top_p": 0.2,
            },
        )
        response_text = self._enforce_output_language(response_text, language)
        response_text = self._clip_text(response_text)

        now = datetime.now(timezone.utc)

        if response_text:
            content = response_text
        elif language == "es":
            content = (
                f"{normalized_parent_content or parent_content}\n\n"
                f"Transformación generada por Ollama ({transformation_type.value})."
            )
        else:
            content = (
                f"{normalized_parent_content or parent_content}\n\n"
                f"Transformation generated by Ollama ({transformation_type.value})."
            )

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
        version_content: str,
        language: str = "en",
    ) -> dict:
        normalized_version_content = self._normalize_input_language(
            version_content,
            language,
        )

        prompt = build_perspective_analysis_prompt(
            version_content=normalized_version_content or version_content,
            perspective=perspective,
            language=language,
        )

        model_name = self._resolve_model(language)
        logger.warning(
            "OLLAMA CALL -> method=%s language=%s model=%s",
            "analyze_perspective",  # cambia esto según el método
            language,
            model_name,
        )
        
        response_text = self.client.generate_text(
            model=model_name,
            prompt=prompt,
            system=self._system_prompt(language),
            options={
                "temperature": 0.1,
                "top_p": 0.2,
            },
        )
        response_text = self._enforce_output_language(response_text, language)
        response_text = self._clip_text(response_text)

        now = datetime.now(timezone.utc)

        if response_text:
            content = response_text
        elif language == "es":
            content = f"Análisis generado por Ollama para '{perspective}'."
        else:
            content = f"Analysis generated by Ollama for '{perspective}'."

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
        version_content: str,
        language: str = "en",
    ) -> dict:
        normalized_version_content = self._normalize_input_language(
            version_content,
            language,
        )

        prompt = build_synthesis_prompt(
            version_content=normalized_version_content or version_content,
            language=language,
        )

        model_name = self._resolve_model(language)
        logger.warning(
            "OLLAMA CALL -> method=%s language=%s model=%s",
            "generate_synthesis",  # cambia esto según el método
            language,
            model_name,
        )
                
        response_text = self.client.generate_text(
            model=model_name,
            prompt=prompt,
            system=self._system_prompt(language),
            options={
                "temperature": 0.1,
                "top_p": 0.2,
            },
        )
        response_text = self._enforce_output_language(response_text, language)
        response_text = self._clip_text(response_text)

        now = datetime.now(timezone.utc)

        parsed = self._parse_synthesis_response(response_text, language=language)

        return {
            "id": f"syn_{uuid4().hex}",
            "summary": parsed["summary"],
            "value_proposition": parsed["value_proposition"],
            "target_audience": parsed["target_audience"],
            "structured_description": parsed["structured_description"],
            "next_steps": parsed["next_steps"],
            "created_at": now,
        }

    def compare_versions(
        self,
        *,
        left_version_content: str,
        right_version_content: str,
        language: str = "en",
    ) -> dict:
        normalized_left = self._normalize_input_language(
            left_version_content,
            language,
        )
        normalized_right = self._normalize_input_language(
            right_version_content,
            language,
        )

        prompt = build_comparison_prompt(
            left_version_content=normalized_left or left_version_content,
            right_version_content=normalized_right or right_version_content,
            language=language,
        )

        model_name = self._resolve_model(language)
        logger.warning(
            "OLLAMA CALL -> method=%s language=%s model=%s",
            "compare_versions",  # cambia esto según el método
            language,
            model_name,
        )
        
        response_text = self.client.generate_text(
            model=model_name,
            prompt=prompt,
            system=self._system_prompt(language),
            options={
                "temperature": 0.1,
                "top_p": 0.2,
            },
        )
        response_text = self._enforce_output_language(response_text, language)
        response_text = self._clip_text(response_text)
        
        now = datetime.now(timezone.utc)

        if response_text:
            comparison_text = response_text
        elif language == "es":
            comparison_text = "Comparación generada por Ollama, pero no se devolvió texto detallado."
        else:
            comparison_text = "Comparison generated by Ollama, but no detailed text was returned."

        return {
            "id": f"cmp_{uuid4().hex}",
            "comparison_text": comparison_text,
            "created_at": now,
        }

    def _parse_variants_response(self, text: str) -> list[dict]:
        if not text.strip():
            return []

        blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
        results: list[dict] = []

        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            title = ""
            description = ""

            for line in lines:
                lowered = line.lower()
                if "title:" in lowered:
                    title = line.split(":", 1)[1].strip()
                elif "description:" in lowered:
                    description = line.split(":", 1)[1].strip()

            if title and description:
                results.append({"title": title, "description": description})
                continue

            if lines:
                first_line = lines[0]
                rest = " ".join(lines[1:]).strip()
                results.append(
                    {
                        "title": first_line[:80],
                        "description": rest or "Generated variant.",
                    }
                )

        return results

    def _parse_synthesis_response(self, text: str, language: str) -> dict:
        result = {
            "summary": "",
            "value_proposition": "",
            "target_audience": "",
            "structured_description": "",
            "next_steps": "",
        }

        if not text.strip():
            return self._fallback_synthesis(language=language)

        label_map = {
            "summary": "summary",
            "resumen": "summary",

            "value proposition": "value_proposition",
            "propuesta de valor": "value_proposition",

            "target audience": "target_audience",
            "publico objetivo": "target_audience",
            "público objetivo": "target_audience",

            "structured description": "structured_description",
            "descripcion estructurada": "structured_description",
            "descripción estructurada": "structured_description",

            "next steps": "next_steps",
            "siguientes pasos": "next_steps",
        }

        current_key: str | None = None

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            normalized = line.lower()

            matched_key = None
            for label, key in label_map.items():
                if normalized.startswith(f"{label}:"):
                    matched_key = key
                    value = line.split(":", 1)[1].strip()
                    if value:
                        if result[key]:
                            result[key] += "\n" + value
                        else:
                            result[key] = value
                    current_key = key
                    break

            if matched_key is not None:
                continue

            # Si no es una nueva etiqueta, pero ya estamos dentro de una sección,
            # asumimos que es continuación multilinea.
            if current_key is not None:
                if result[current_key]:
                    result[current_key] += "\n" + line
                else:
                    result[current_key] = line

        fallback = self._fallback_synthesis(language=language)
        for key, value in result.items():
            if not value.strip():
                result[key] = fallback[key]

        return result

    def _fallback_variants(self, now: datetime, language: str) -> list[dict]:
        if language == "es":
            return [
                {
                    "id": f"var_{uuid4().hex}",
                    "title": "Variante generada 1",
                    "description": "Variante generada por Ollama (fallback).",
                    "order_index": 1,
                    "created_at": now,
                },
                {
                    "id": f"var_{uuid4().hex}",
                    "title": "Variante generada 2",
                    "description": "Variante generada por Ollama (fallback).",
                    "order_index": 2,
                    "created_at": now,
                },
                {
                    "id": f"var_{uuid4().hex}",
                    "title": "Variante generada 3",
                    "description": "Variante generada por Ollama (fallback).",
                    "order_index": 3,
                    "created_at": now,
                },
            ]

        return [
            {
                "id": f"var_{uuid4().hex}",
                "title": "Generated variant 1",
                "description": "Variant generated by Ollama (fallback).",
                "order_index": 1,
                "created_at": now,
            },
            {
                "id": f"var_{uuid4().hex}",
                "title": "Generated variant 2",
                "description": "Variant generated by Ollama (fallback).",
                "order_index": 2,
                "created_at": now,
            },
            {
                "id": f"var_{uuid4().hex}",
                "title": "Generated variant 3",
                "description": "Variant generated by Ollama (fallback).",
                "order_index": 3,
                "created_at": now,
            },
        ]

    def _fallback_synthesis(self, language: str) -> dict:
        if language == "es":
            return {
                "summary": "Resumen generado por Ollama (fallback).",
                "value_proposition": "Propuesta de valor generada por Ollama (fallback).",
                "target_audience": "Público objetivo generado por Ollama (fallback).",
                "structured_description": "Descripción estructurada generada por Ollama (fallback).",
                "next_steps": "Siguientes pasos generados por Ollama (fallback).",
            }

        return {
            "summary": "Summary generated by Ollama (fallback).",
            "value_proposition": "Value proposition generated by Ollama (fallback).",
            "target_audience": "Target audience generated by Ollama (fallback).",
            "structured_description": "Structured description generated by Ollama (fallback).",
            "next_steps": "Next steps generated by Ollama (fallback).",
        }
    
    def _normalize_input_language(self, text: str | None, language: str) -> str | None:
        if text is None:
            return None

        cleaned = text.strip()
        if not cleaned:
            return text

        detected = detect_language(cleaned)

        if language == "es" and detected == "es":
            return cleaned

        if language == "en" and detected == "en":
            return cleaned

        rewrite_prompt = build_language_rewrite_prompt(
            text=cleaned,
            language=language,
        )

        model_name = self._resolve_model(language)
        logger.warning(
            "OLLAMA CALL -> method=%s language=%s model=%s",
            "normalize_input_languagen",  # cambia esto según el método
            language,
            model_name,
        )
        
        rewritten = self.client.generate_text(
            model=model_name,
            prompt=rewrite_prompt,
            system=self._system_prompt(language),
            options={
                "temperature": 0.0,
                "top_p": 0.1,
            },
        ).strip()

        if rewritten:
            rewritten_detected = detect_language(rewritten)

            if language == "es" and rewritten_detected == "es":
                return rewritten

            if language == "en" and rewritten_detected == "en":
                return rewritten

        return cleaned
    
    def _enforce_output_language(self, text: str, language: str) -> str:
        if not text.strip():
            return text

        detected = detect_language(text)

        if language == "es" and detected == "es":
            return text

        if language == "en" and detected == "en":
            return text

        current_text = text

        for _ in range(3):
            rewrite_prompt = build_language_rewrite_prompt(
                text=current_text,
                language=language,
            )

            model_name = self._resolve_model(language)
            logger.warning(
                "OLLAMA CALL -> method=%s language=%s model=%s",
                "enforce_output_language",  # cambia esto según el método
                language,
                model_name,
            )
            
            rewritten = self.client.generate_text(
                model=model_name,
                prompt=rewrite_prompt,
                system=self._system_prompt(language),
                options={
                    "temperature": 0.0,
                    "top_p": 0.1,
                },
            ).strip()

            if not rewritten:
                break

            rewritten_detected = detect_language(rewritten)

            if language == "es" and rewritten_detected == "es":
                return rewritten

            if language == "en" and rewritten_detected == "en":
                return rewritten

            current_text = rewritten

        return current_text