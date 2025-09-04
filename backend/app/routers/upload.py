import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from ..services.rag_store import upsert_document

router = APIRouter()


@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")
    pdf_bytes = await file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF")
    try:
        result = upsert_document(text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    result["filename"] = file.filename
    return result
