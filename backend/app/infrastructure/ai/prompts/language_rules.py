from __future__ import annotations


def build_language_instruction(language: str) -> str:
    if language == "es":
        return (
            "CRITICAL LANGUAGE RULE: Respond only in Spanish. "
            "Every sentence, title, label, and paragraph must be in Spanish. "
            "Do not mix Spanish with English under any circumstance. "
            "If the input contains English fragments, still answer entirely in Spanish."
        )

    return (
        "CRITICAL LANGUAGE RULE: Respond only in English. "
        "Every sentence, title, label, and paragraph must be in English. "
        "Do not mix English with Spanish under any circumstance. "
        "If the input contains Spanish fragments, still answer entirely in English."
    )