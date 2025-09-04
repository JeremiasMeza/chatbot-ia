import uuid
from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# doc_id -> {"chunks": list[str], "vectorizer": TfidfVectorizer, "matrix": csr_matrix}
DOCUMENTS: Dict[str, Dict] = {}


def split_text(text: str, chunk_size: int = 500) -> list[str]:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def upsert_document(text: str) -> dict:
    chunks = [c.strip() for c in split_text(text) if c and c.strip()]
    if not chunks:
        raise ValueError("No se encontró texto válido en el documento")
    vectorizer = TfidfVectorizer().fit(chunks)
    matrix = vectorizer.transform(chunks)
    doc_id = str(uuid.uuid4())
    DOCUMENTS[doc_id] = {
        "chunks": chunks,
        "vectorizer": vectorizer,
        "matrix": matrix,
    }
    return {"doc_id": doc_id, "upserted": len(chunks)}


def query_document(doc_id: str, prompt: str) -> str:
    data = DOCUMENTS.get(doc_id)
    if not data:
        return "No hay documento indexado."
    vec = data["vectorizer"].transform([prompt])
    sims = cosine_similarity(vec, data["matrix"])[0]
    idx = sims.argmax()
    return data["chunks"][idx]
