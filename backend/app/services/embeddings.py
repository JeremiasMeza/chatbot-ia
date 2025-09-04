import os
from typing import List
from sentence_transformers import SentenceTransformer

_EMBED_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
_model: SentenceTransformer | None = None

def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_EMBED_MODEL_NAME)
    return _model

def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedder()
    # Convertimos a listas nativas de floats (no numpy arrays) para chroma
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]
