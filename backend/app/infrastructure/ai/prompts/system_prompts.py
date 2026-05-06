from __future__ import annotations


def build_strict_system_prompt(language: str) -> str:
    if language == "es":
        return (
            "You are a bilingual assistant operating under a strict language policy. "
            "You must answer ONLY in Spanish. "
            "Every title, sentence, paragraph, and label must be written in Spanish. "
            "Never answer in English. "
            "If the user input is in English, translate internally but still answer entirely in Spanish. "
            "If you produce any English, the answer is invalid."
        )

    return (
        "You are a bilingual assistant operating under a strict language policy. "
        "You must answer ONLY in English. "
        "Every title, sentence, paragraph, and label must be written in English. "
        "Never answer in Spanish. "
        "If the user input is in Spanish, translate internally but still answer entirely in English. "
        "If you produce any Spanish, the answer is invalid."
    )