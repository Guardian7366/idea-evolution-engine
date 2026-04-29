"""
test_mappers.py — Unit tests for all AI response mappers.

Tests run without Ollama using static JSON fixtures.
Each mapper is tested for:
  - happy path (valid JSON)
  - markdown fence wrapping (```json ... ```)
  - malformed / empty JSON → fallback
  - missing required keys → fallback
  - fallback UUID uniqueness (variant_mapper bug regression)
  - logging of fallback paths
"""

import json
import logging
import pytest

from app.infrastructure.ai.mappers.base import coerce_str_list, extract_json, LLMParseError
from app.infrastructure.ai.mappers.variant_mapper import map_variants
from app.infrastructure.ai.mappers.analysis_mapper import map_comparison, map_perspective
from app.infrastructure.ai.mappers.synthesis_mapper import map_synthesis
from app.infrastructure.ai.mappers.transformation_mapper import map_transformation


# ── Helpers ───────────────────────────────────────────────────────────────────

def as_json(data: dict) -> str:
    return json.dumps(data)


def as_fenced(data: dict) -> str:
    return f"```json\n{json.dumps(data)}\n```"


# ── base.py ───────────────────────────────────────────────────────────────────

class TestExtractJson:
    def test_raw_json(self):
        assert extract_json('{"a": 1}') == {"a": 1}

    def test_markdown_fence(self):
        assert extract_json('```json\n{"b": 2}\n```') == {"b": 2}

    def test_embedded_in_text(self):
        assert extract_json('some text {"c": 3} more text') == {"c": 3}

    def test_raises_on_unparseable(self):
        with pytest.raises(LLMParseError):
            extract_json("this is not json at all <<<")


class TestCoerceStrList:
    def test_clean_list(self):
        assert coerce_str_list(["a", "b", "c"]) == ["a", "b", "c"]

    def test_strips_whitespace(self):
        assert coerce_str_list(["  a  ", "b"]) == ["a", "b"]

    def test_filters_blank_entries(self):
        assert coerce_str_list(["a", "", "  ", "b"]) == ["a", "b"]

    def test_non_list_returns_empty(self):
        assert coerce_str_list(None) == []
        assert coerce_str_list("a string") == []
        assert coerce_str_list(42) == []

    def test_coerces_non_strings(self):
        assert coerce_str_list([1, 2, 3]) == ["1", "2", "3"]


# ── variant_mapper ─────────────────────────────────────────────────────────────

VALID_VARIANTS_PAYLOAD = {
    "variants": [
        {"title": "Expansion", "content": "Wider scope.", "variant_type": "expansion"},
        {"title": "Focus", "content": "Sharper target.", "variant_type": "focus"},
        {"title": "Twist", "content": "Unexpected angle.", "variant_type": "creative_twist"},
    ]
}


class TestMapVariants:
    def test_happy_path_returns_three_items(self):
        result = map_variants(as_json(VALID_VARIANTS_PAYLOAD))
        assert len(result) == 3

    def test_happy_path_preserves_titles(self):
        result = map_variants(as_json(VALID_VARIANTS_PAYLOAD))
        assert [v.title for v in result] == ["Expansion", "Focus", "Twist"]

    def test_happy_path_preserves_types(self):
        result = map_variants(as_json(VALID_VARIANTS_PAYLOAD))
        assert [v.variant_type for v in result] == ["expansion", "focus", "creative_twist"]

    def test_each_item_has_unique_variant_id(self):
        result = map_variants(as_json(VALID_VARIANTS_PAYLOAD))
        assert len({v.variant_id for v in result}) == 3

    def test_markdown_fence_accepted(self):
        result = map_variants(as_fenced(VALID_VARIANTS_PAYLOAD))
        assert len(result) == 3
        assert result[0].title == "Expansion"

    def test_empty_json_returns_fallback(self):
        result = map_variants("{}")
        assert len(result) == 3

    def test_malformed_json_returns_fallback(self):
        result = map_variants("not json at all <<<")
        assert len(result) == 3

    def test_fallback_ids_are_unique_across_calls(self):
        """Regression: fallback used to reuse module-level fixed UUIDs."""
        ids_a = {v.variant_id for v in map_variants("{}")}
        ids_b = {v.variant_id for v in map_variants("{}")}
        assert ids_a.isdisjoint(ids_b), "Fallback calls must not share variant IDs"

    def test_invalid_variant_type_coerced_to_expansion(self):
        payload = {
            "variants": [
                {"title": "A", "content": "Content A.", "variant_type": "unknown_type"},
                {"title": "B", "content": "Content B.", "variant_type": "focus"},
                {"title": "C", "content": "Content C.", "variant_type": "creative_twist"},
            ]
        }
        result = map_variants(as_json(payload))
        assert result[0].variant_type == "expansion"

    def test_fewer_than_three_variants_padded_with_fresh_fallback(self):
        payload = {
            "variants": [
                {"title": "Only one", "content": "Just one.", "variant_type": "expansion"},
            ]
        }
        result = map_variants(as_json(payload))
        assert len(result) == 3
        assert result[0].title == "Only one"
        # Padded items must have fresh IDs (not overlap with the real one)
        real_id = result[0].variant_id
        assert result[1].variant_id != real_id
        assert result[2].variant_id != real_id

    def test_title_truncated_at_60_chars(self):
        payload = {
            "variants": [
                {"title": "A" * 100, "content": "Content.", "variant_type": "expansion"},
                {"title": "B", "content": "Content.", "variant_type": "focus"},
                {"title": "C", "content": "Content.", "variant_type": "creative_twist"},
            ]
        }
        result = map_variants(as_json(payload))
        assert len(result[0].title) <= 60

    def test_fallback_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="app.infrastructure.ai.mappers.variant_mapper"):
            map_variants("{}")
        assert any("fallback" in r.message.lower() or "ausente" in r.message.lower()
                   for r in caplog.records)


# ── analysis_mapper ────────────────────────────────────────────────────────────

VALID_COMPARISON_PAYLOAD = {
    "summary": "Version B is more refined.",
    "strengths_version_a": ["Original intent preserved", "Simpler language"],
    "strengths_version_b": ["Clearer structure", "More actionable"],
    "key_differences": ["A is broader", "B is more focused"],
    "recommendation": "Proceed with Version B.",
}

VALID_PERSPECTIVE_PAYLOAD = {
    "summary": "The idea is technically feasible.",
    "observations": ["Low complexity", "Existing tooling available", "Small team sufficient"],
    "suggestion": "Build a quick prototype to validate.",
}


class TestMapComparison:
    def test_happy_path_returns_result(self):
        result = map_comparison(as_json(VALID_COMPARISON_PAYLOAD))
        assert result.summary == "Version B is more refined."
        assert result.recommendation == "Proceed with Version B."

    def test_happy_path_lists_preserved(self):
        result = map_comparison(as_json(VALID_COMPARISON_PAYLOAD))
        assert result.strengths_version_a == ["Original intent preserved", "Simpler language"]
        assert result.key_differences == ["A is broader", "B is more focused"]

    def test_markdown_fence_accepted(self):
        result = map_comparison(as_fenced(VALID_COMPARISON_PAYLOAD))
        assert result.summary == "Version B is more refined."

    def test_empty_json_returns_fallback(self):
        result = map_comparison("{}")
        assert "Both versions" in result.summary

    def test_malformed_json_returns_fallback(self):
        result = map_comparison("garbage !!!")
        assert result.summary != ""

    def test_missing_summary_returns_fallback(self):
        payload = {k: v for k, v in VALID_COMPARISON_PAYLOAD.items() if k != "summary"}
        result = map_comparison(as_json(payload))
        assert "Both versions" in result.summary

    def test_fallback_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="app.infrastructure.ai.mappers.analysis_mapper"):
            map_comparison("{}")
        assert len(caplog.records) > 0


class TestMapPerspective:
    def test_happy_path(self):
        result = map_perspective(as_json(VALID_PERSPECTIVE_PAYLOAD), "feasibility")
        assert result.perspective_type == "feasibility"
        assert result.summary == "The idea is technically feasible."
        assert result.observations == ["Low complexity", "Existing tooling available", "Small team sufficient"]

    def test_markdown_fence_accepted(self):
        result = map_perspective(as_fenced(VALID_PERSPECTIVE_PAYLOAD), "risks")
        assert result.perspective_type == "risks"

    def test_empty_json_returns_fallback(self):
        result = map_perspective("{}", "innovation")
        assert result.perspective_type == "innovation"
        assert "could not be completed" in result.summary

    def test_malformed_json_returns_fallback(self):
        result = map_perspective("{{bad json", "user_value")
        assert result.perspective_type == "user_value"

    def test_fallback_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="app.infrastructure.ai.mappers.analysis_mapper"):
            map_perspective("{}", "feasibility")
        assert len(caplog.records) > 0


# ── synthesis_mapper ──────────────────────────────────────────────────────────

VALID_SYNTHESIS_PAYLOAD = {
    "title": "Final Synthesized Concept",
    "core_concept": "An AI tool that accelerates idea refinement.",
    "value_proposition": "Reduces ideation time by 80%.",
    "recommended_next_step": "Build an MVP with three core features.",
    "notes": ["Keep scope tight", "Validate with 5 users first", "Ship in 6 weeks"],
}


class TestMapSynthesis:
    def test_happy_path(self):
        result = map_synthesis(as_json(VALID_SYNTHESIS_PAYLOAD), total_versions=3)
        assert result.title == "Final Synthesized Concept"
        assert result.core_concept == "An AI tool that accelerates idea refinement."
        assert result.notes == ["Keep scope tight", "Validate with 5 users first", "Ship in 6 weeks"]

    def test_title_truncated_at_80_chars(self):
        payload = {**VALID_SYNTHESIS_PAYLOAD, "title": "T" * 100}
        result = map_synthesis(as_json(payload), total_versions=1)
        assert len(result.title) <= 80

    def test_markdown_fence_accepted(self):
        result = map_synthesis(as_fenced(VALID_SYNTHESIS_PAYLOAD), total_versions=2)
        assert result.title == "Final Synthesized Concept"

    def test_empty_json_returns_fallback(self):
        result = map_synthesis("{}", total_versions=4)
        assert result.title == "Final Idea Synthesis"
        assert "4 version" in result.notes[0]

    def test_malformed_json_returns_fallback(self):
        result = map_synthesis("not json", total_versions=1)
        assert result.recommended_next_step != ""

    def test_fallback_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="app.infrastructure.ai.mappers.synthesis_mapper"):
            map_synthesis("{}", total_versions=1)
        assert len(caplog.records) > 0


# ── transformation_mapper ──────────────────────────────────────────────────────

VALID_TRANSFORMATION_PAYLOAD = {
    "title": "Refined Direction",
    "content": "The idea now focuses on a narrower user segment.",
}


class TestMapTransformation:
    def test_happy_path(self):
        result = map_transformation(as_json(VALID_TRANSFORMATION_PAYLOAD), "refine", "Make it simpler")
        assert result["title"] == "Refined Direction"
        assert result["content"] == "The idea now focuses on a narrower user segment."

    def test_title_truncated_at_80_chars(self):
        payload = {**VALID_TRANSFORMATION_PAYLOAD, "title": "X" * 100}
        result = map_transformation(as_json(payload), "evolve", "instruction")
        assert len(result["title"]) <= 80

    def test_markdown_fence_accepted(self):
        result = map_transformation(as_fenced(VALID_TRANSFORMATION_PAYLOAD), "refine", "instruction")
        assert result["title"] == "Refined Direction"

    def test_empty_json_returns_fallback_with_type_prefix(self):
        result = map_transformation("{}", "evolve", "Make it bigger")
        assert result["title"] == "Evolved Version"
        assert "evolve" in result["content"].lower()

    def test_malformed_json_returns_fallback(self):
        result = map_transformation("bad json!!", "refine", "instruction")
        assert result["title"] == "Refined Version"

    def test_unknown_type_uses_transformed_prefix(self):
        result = map_transformation("{}", "unknown_op", "some instruction")
        assert result["title"] == "Transformed Version"

    def test_missing_content_returns_fallback(self):
        payload = {"title": "Has title but no content"}
        result = map_transformation(as_json(payload), "mutate", "instruction")
        assert result["title"] == "Mutated Version"

    def test_fallback_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="app.infrastructure.ai.mappers.transformation_mapper"):
            map_transformation("{}", "refine", "instruction")
        assert len(caplog.records) > 0


# ── llm_client exception types ────────────────────────────────────────────────

class TestLLMClientExceptionTypes:
    """Verify the exception hierarchy is importable and correctly typed."""

    def test_exception_types_importable(self):
        from app.infrastructure.ai.llm_client import (
            OllamaUnavailableError,
            OllamaTimeoutError,
            OllamaHTTPError,
            OllamaResponseError,
        )
        assert issubclass(OllamaUnavailableError, RuntimeError)
        assert issubclass(OllamaTimeoutError, RuntimeError)
        assert issubclass(OllamaHTTPError, RuntimeError)
        assert issubclass(OllamaResponseError, RuntimeError)

    def test_http_error_stores_code_and_body(self):
        from app.infrastructure.ai.llm_client import OllamaHTTPError
        exc = OllamaHTTPError(404, "model not found")
        assert exc.code == 404
        assert exc.body == "model not found"
        assert "404" in str(exc)
