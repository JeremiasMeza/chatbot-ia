from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import health, chat, docs
from app.api.routers import ask as ask_router

app = FastAPI(title="Chatbot Backend", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod: restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router,   prefix="/api", tags=["chat"])
app.include_router(docs.router,   prefix="/api/docs", tags=["docs"])
app.include_router(ask_router.router, prefix="/api", tags=["ask"])

@app.get("/")
def root():
    return {"name": "Chatbot Backend", "status": "ok"}
