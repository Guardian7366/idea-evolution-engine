from __future__ import annotations

import re


SPANISH_HINTS = {
    "idea",
    "ideas",
    "quiero",
    "quisiera",
    "crear",
    "hacer",
    "desarrollar",
    "construir",
    "mejorar",
    "generar",
    "necesito",
    "busco",
    "debe",
    "deberia",
    "debería",
    "pueda",
    "puedo",
    "tenga",
    "tener",
    "relacionado",
    "relacionada",
    "relacionados",
    "relacionadas",
    "innovador",
    "innovadora",
    "innovadores",
    "innovadoras",
    "aplicacion",
    "aplicación",
    "plataforma",
    "sistema",
    "herramienta",
    "proyecto",
    "producto",
    "servicio",
    "funcion",
    "función",
    "funciones",
    "usuario",
    "usuarios",
    "ejercicio",
    "ejercicios",
    "entrenamiento",
    "salud",
    "rutina",
    "rutinas",
    "bienestar",
    "deporte",
    "deportes",
    "bote",
    "barco",
    "embarcacion",
    "embarcación",
    "vehiculo",
    "vehículo",
    "fuego",
    "incendio",
    "incendios",
    "explosion",
    "explosión",
    "explosiones",
    "seguridad",
    "proteccion",
    "protección",
    "rescate",
    "emergencia",
    "emergencias",
    "version",
    "versión",
    "variantes",
    "sintesis",
    "síntesis",
    "analisis",
    "análisis",
    "comparacion",
    "comparación",
    "comparar",
    "refinar",
    "refinamiento",
    "mutacion",
    "mutación",
    "evolucion",
    "evolución",
    "para",
    "con",
    "sin",
    "tambien",
    "también",
    "porque",
    "como",
    "ademas",
    "además",
    "entre",
    "hacia",
    "desde",
    "sobre",
    "contra",
}


def detect_language(text: str | None) -> str:
    if not text:
        return "en"

    lowered = text.lower().strip()

    if re.search(r"[áéíóúñ¿¡]", lowered):
        return "es"

    tokens = re.findall(r"[a-záéíóúñ]+", lowered)
    if not tokens:
        return "en"

    spanish_matches = sum(1 for token in tokens if token in SPANISH_HINTS)
    ratio = spanish_matches / max(len(tokens), 1)

    if spanish_matches >= 2:
        return "es"

    if len(tokens) >= 6 and spanish_matches >= 1:
        return "es"

    if ratio >= 0.12:
        return "es"

    return "en"


def resolve_language(
    *,
    preferred_language: str | None,
    fallback_text: str | None,
) -> str:
    normalized = (preferred_language or "auto").strip().lower()

    if normalized in {"es", "en"}:
        return normalized

    return detect_language(fallback_text)