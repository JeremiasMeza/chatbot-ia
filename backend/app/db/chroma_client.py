import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
import chromadb

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "kb_default")

_client: Optional[chromadb.PersistentClient] = None
_collection = None

def get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return _client

def get_collection():
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection(name=CHROMA_COLLECTION)
    return _collection

def upsert_documents(
    documents: List[str],
    embeddings: List[List[float]],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    doc_prefix: str = "doc"
) -> int:
    col = get_collection()
    ids = [f"{doc_prefix}-{uuid.uuid4().hex}-{i}" for i in range(len(documents))]
    col.upsert(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    return len(ids)

def query_similar(
    query_embeddings: List[List[float]],
    top_k: int = 4,
) -> Tuple[List[str], List[Dict[str, Any]], List[float]]:
    """
    Retorna (documents, metadatas, distances) para el/los embeddings de consulta.
    Para 1 consulta, devolvemos la primera lista.
    """
    col = get_collection()
    res = col.query(
        query_embeddings=query_embeddings,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    # Estructura: res["documents"] -> List[List[str]] (por cada query)
    docs = res.get("documents", [[]])[0] if res.get("documents") else []
    metas = res.get("metadatas", [[]])[0] if res.get("metadatas") else []
    dists = res.get("distances", [[]])[0] if res.get("distances") else []
    return docs, metas, dists

def count_documents() -> int:
    col = get_collection()
    return col.count()

def peek_documents(limit: int = 3):
    col = get_collection()
    return col.get(include=["documents", "metadatas"], limit=limit)

