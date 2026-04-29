"""
test_live_models.py — Prueba en vivo contra Ollama con ambos modelos.

Requiere Ollama corriendo en localhost:11434 con los modelos descargados:
    ollama pull llama3.1
    ollama pull qwen2.5

Ejecución:
    python tests/test_live_models.py
"""

import json
import sys
import time
import urllib.error
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"

PROMPT_SYSTEM = (
    "You are a creative idea consultant. "
    "Respond ONLY with a valid JSON object, no text outside it."
)

PROMPT_USER = (
    "Generate 3 innovative startup ideas in the field of sustainable technology. "
    "Return JSON in this exact structure:\n"
    '{"ideas": [{"title": "...", "description": "...", "key_benefit": "..."}]}'
)

MODELS = {
    "capable (llama3.1:latest)": "llama3.1:latest",
    "fast    (qwen2.5)":         "qwen2.5",
}


def check_ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434/", timeout=3)
        return True
    except Exception:
        return False


def check_model_available(model: str) -> bool:
    try:
        resp = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
        data = json.loads(resp.read().decode())
        names = [m["name"] for m in data.get("models", [])]
        # Match on base name (e.g. "llama3.1:8b" matches "llama3.1:8b-instruct-...")
        return any(model.split(":")[0] in n for n in names)
    except Exception:
        return False


def call_model(model: str, timeout: float = 180.0) -> tuple[str, float]:
    """Returns (raw_response_text, elapsed_seconds)."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM},
            {"role": "user",   "content": PROMPT_USER},
        ],
        "stream": False,
        "format": "json",
    }).encode()

    req = urllib.request.Request(
        url=OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = json.loads(resp.read().decode())
            content = raw["message"]["content"]
            elapsed = time.perf_counter() - t0
            return content, elapsed
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"No se pudo conectar a Ollama: {exc.reason}") from exc


def print_result(label: str, raw: str, elapsed: float) -> None:
    separator = "─" * 60
    print(f"\n{separator}")
    print(f"  MODELO: {label}")
    print(f"  Tiempo: {elapsed:.1f}s")
    print(separator)
    try:
        parsed = json.loads(raw)
        ideas = parsed.get("ideas", [])
        for i, idea in enumerate(ideas, 1):
            print(f"\n  [{i}] {idea.get('title', '—')}")
            print(f"      {idea.get('description', '—')}")
            print(f"      Beneficio: {idea.get('key_benefit', '—')}")
    except json.JSONDecodeError:
        print(f"  (respuesta no es JSON válido)\n  {raw[:300]}")
    print()


def main() -> None:
    print("\n=== TEST EN VIVO — IDEA EVOLUTION ENGINE ===")
    print(f"Prompt: {PROMPT_USER[:80]}...\n")

    if not check_ollama_running():
        print("ERROR: Ollama no está corriendo en localhost:11434")
        print()
        print("Para iniciar Ollama:")
        print("  Windows: abrir la aplicación Ollama desde el menú de inicio")
        print("  o ejecutar:  ollama serve")
        print()
        print("Para descargar los modelos:")
        print("  ollama pull llama3.1")
        print("  ollama pull qwen2.5")
        sys.exit(1)

    results = {}
    for label, model in MODELS.items():
        if not check_model_available(model):
            print(f"AVISO: modelo '{model}' no descargado. Ejecuta: ollama pull {model}")
            results[label] = None
            continue

        print(f"Consultando {label}...", end=" ", flush=True)
        try:
            raw, elapsed = call_model(model)
            results[label] = (raw, elapsed)
            print(f"OK ({elapsed:.1f}s)")
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            results[label] = None

    print("\n" + "=" * 60)
    print("  RESPUESTAS")
    print("=" * 60)

    for label, result in results.items():
        if result is None:
            print(f"\n[{label}] — sin respuesta")
        else:
            raw, elapsed = result
            print_result(label, raw, elapsed)

    # Comparación de tiempos
    times = {k: v[1] for k, v in results.items() if v is not None}
    if len(times) == 2:
        vals = list(times.values())
        ratio = max(vals) / min(vals)
        print("─" * 60)
        print(f"  El modelo rapido fue {ratio:.1f}x mas rapido que el lento")
        print("─" * 60)


if __name__ == "__main__":
    main()
