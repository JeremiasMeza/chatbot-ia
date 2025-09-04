from fastapi import APIRouter
from pydantic import BaseModel
from ..services.rag_store import query_document

router = APIRouter()


class ChatRequest(BaseModel):
    model: str
    prompt: str
    doc_id: str | None = None


@router.post("/chat/")
async def chat(req: ChatRequest):
    if req.doc_id:
        context = query_document(req.doc_id, req.prompt)
        reply = f"Fragmento relevante del documento: {context}"
    else:
        reply = "No hay documento indexado."
    return {"message": {"role": "ai", "content": reply}}
