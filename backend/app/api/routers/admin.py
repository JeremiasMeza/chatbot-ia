from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.text import pdf_bytes_to_text, chunk_text, prepare_chunks_with_meta
from app.services.embeddings import embed_texts
from app.db.chroma_client import upsert_documents

router = APIRouter()

@router.post("/admin/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        pdf_bytes = await file.read()
        full_text = pdf_bytes_to_text(pdf_bytes)
        if not full_text:
            raise HTTPException(status_code=400, detail="No extractable text found in the PDF")

        chunks = chunk_text(full_text, max_chars=800, overlap=150)
        texts, metas = prepare_chunks_with_meta(chunks, filename=file.filename)
        vecs = embed_texts(texts)
        count = upsert_documents(texts, vecs, metas, doc_prefix=file.filename.rsplit(".", 1)[0])

        return {
            "status": "ok",
            "filename": file.filename,
            "chunks": len(chunks),
            "upserted": count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
