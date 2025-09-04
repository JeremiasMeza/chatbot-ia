from typing import List, Dict, Any, Optional
from app.services.embeddings import embed_texts
from app.db.chroma_client import query_similar
from app.services.ollama_client import query_ollama

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer ONLY using the provided context. "
    "If the answer is not in the context, say you don't have that information."
)

def build_prompt(question: str, contexts: List[str]) -> str:
    context_block = "\n\n".join([f"- {c}" for c in contexts])
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n\n"
        f"Answer in Spanish, concise and precise."
    )
    return prompt

def answer_with_context(
    question: str,
    top_k: int = 4,
    score_threshold: Optional[float] = None
) -> Dict[str, Any]:

    q_vec = embed_texts([question])


    docs, metas, dists = query_similar(q_vec, top_k=top_k)

    if score_threshold is not None:
        filtered = [(d, m, dist) for d, m, dist in zip(docs, metas, dists) if dist <= score_threshold]
    else:
        filtered = list(zip(docs, metas, dists))

    if not filtered:
        # Sin contexto suficiente
        prompt = build_prompt(question, [])
        reply = query_ollama(prompt)
        return {"reply": reply.strip(), "contexts": [], "distances": []}

    # 4) Tomar contextos
    contexts = [d for d, _, _ in filtered]
    final_prompt = build_prompt(question, contexts)
    reply = query_ollama(final_prompt).strip()

    return {
        "reply": reply,
        "contexts": contexts,
        "metas": [m for _, m, _ in filtered],
        "distances": [dist for _, _, dist in filtered],
    }
