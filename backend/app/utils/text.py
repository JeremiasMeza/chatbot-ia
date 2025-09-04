from typing import List, Tuple
from pypdf import PdfReader
from io import BytesIO

def pdf_bytes_to_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        parts.append(txt)
    return "\n".join(parts).strip()

def chunk_text(text: str, max_chars: int = 800, overlap: int = 150) -> List[str]:
    """
    Trocea por caracteres (simple y efectivo).
    """
    chunks: List[str] = []
    n = len(text)
    start = 0
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks

def prepare_chunks_with_meta(chunks: List[str], filename: str) -> Tuple[List[str], list]:
    metadatas = [{"source": filename, "type": "pdf", "index": i} for i, _ in enumerate(chunks)]
    return chunks, metadatas
