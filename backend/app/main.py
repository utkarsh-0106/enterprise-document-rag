from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.routers.documents import router as documents_router
from backend.app.routers.rag import router as rag_router

app = FastAPI(
    title="Enterprise Document RAG Knowledge Base",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(rag_router, prefix="/api")
