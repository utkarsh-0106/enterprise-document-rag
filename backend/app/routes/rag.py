from fastapi import APIRouter
from backend.app.services.rag import query_rag

router = APIRouter()

@router.post("/")
async def rag_endpoint(question: str, user_id: int):
    result = await query_rag(question, user_id)
    return result