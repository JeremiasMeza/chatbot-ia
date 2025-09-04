from fastapi import APIRouter, HTTPException
from app.services.ollama_client import ollama_health

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/health/full")
def health_full():
    try:
        o = ollama_health()
        return {"status": "ok", "ollama": o}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama unreachable: {e}")
