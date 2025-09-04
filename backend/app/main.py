from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.upload import router as upload_router
from .routers.chat import router as chat_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/models/")
async def list_models():
    return {"models": [{"name": "dummy"}]}

app.include_router(upload_router)
app.include_router(chat_router)
