from fastapi import FastAPI
from backend.app.routes.rag import router

app = FastAPI()

app.include_router(router, prefix="/rag")