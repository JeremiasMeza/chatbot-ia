# Chatbot IA Backend

This project exposes a simple API for uploading PDF documents and asking
questions based on their content.

## Endpoints

- `POST /api/docs/upload` — Upload a PDF file. The text is split into chunks,
  embedded and stored for later retrieval.
- `POST /api/ask` — Ask a question using the information extracted from the
  uploaded documents. Returns the answer and the source text snippets.
- `POST /api/chat` — Free-form chat with the language model without using the
  document context.
- `GET /api/health` — Basic health check.

## Development

Install dependencies from `backend/requirements.txt` and run the FastAPI app:

```bash
uvicorn app.main:app --reload
```
