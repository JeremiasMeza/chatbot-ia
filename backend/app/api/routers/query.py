from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, SourceChunk
from app.services.rag_pipeline import answer_with_context

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        result = answer_with_context(
            question=req.question.strip(),
            top_k=req.top_k,
            score_threshold=req.score_threshold
        )
        sources = []
        contexts = result.get("contexts", [])
        metas = result.get("metas", [{} for _ in contexts])
        dists = result.get("distances", [None for _ in contexts])

        for text, meta, dist in zip(contexts, metas, dists):
            sources.append(SourceChunk(
                text=text,
                source=meta.get("source"),
                index=meta.get("index"),
                distance=dist
            ))
        return QueryResponse(reply=result["reply"], sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
