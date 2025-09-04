import os
import httpx

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

def query_ollama(prompt: str) -> str:
    """
    Llama a Ollama /api/generate con stream desactivado para obtener una sola respuesta JSON.
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "").strip()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Ollama request failed: {e}") from e
def ollama_health() -> dict:
    url = f"{OLLAMA_HOST}/api/tags"
    with httpx.Client(timeout=10.0) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
    models = [m.get("model") for m in data.get("models", []) if isinstance(m, dict)]
    return {"reachable": True, "models": models, "using": OLLAMA_MODEL, "has_model": OLLAMA_MODEL in models}

