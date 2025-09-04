from typing import List, Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

from typing import List, Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    top_k: int = 4
    score_threshold: Optional[float] = None  # ej: 0.2 (opcional)

class SourceChunk(BaseModel):
    text: str
    source: Optional[str] = None
    index: Optional[int] = None
    distance: Optional[float] = None

class QueryResponse(BaseModel):
    reply: str
    sources: List[SourceChunk] = []
