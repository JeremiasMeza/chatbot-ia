
from app.main import app

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
import io
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for indexed documents
# doc_id -> {"chunks": [str], "vectorizer": TfidfVectorizer, "matrix": csr_matrix, "filename": str}
DOCS = {}


@app.get("/models/")
async def list_models():
    """Return available model names for the frontend selector."""
    return {"models": [{"name": "dummy"}]}


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Receive a PDF, split it into chunks and index via TF-IDF."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")

    pdf_bytes = await file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF")

    chunk_size = 500
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    vectorizer = TfidfVectorizer().fit(chunks)
    matrix = vectorizer.transform(chunks)

    doc_id = str(uuid4())
    DOCS[doc_id] = {
        "chunks": chunks,
        "vectorizer": vectorizer,
        "matrix": matrix,
        "filename": file.filename,
    }

    return {"doc_id": doc_id, "filename": file.filename, "upserted": len(chunks)}


class ChatRequest(BaseModel):
    model: str
    prompt: str
    doc_id: str | None = None


@app.post("/chat/")
async def chat(req: ChatRequest):
    """Simple retrieval: return the most relevant chunk for the prompt."""
    if req.doc_id and req.doc_id in DOCS:
        data = DOCS[req.doc_id]
        vec = data["vectorizer"].transform([req.prompt])
        sims = cosine_similarity(vec, data["matrix"])[0]
        idx = sims.argmax()
        context = data["chunks"][idx]
        reply = f"Fragmento relevante del documento: {context}"
    else:
        reply = "No hay documento indexado."

    return {"message": {"role": "ai", "content": reply}}
