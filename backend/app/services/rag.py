from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from backend.app.schemas.rag import RagRequest, RagResponse
from backend.app.settings import settings
from backend.app.services.vector_store import similarity_search


def _get_llm() -> ChatOpenAI:
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured",
        )

    return ChatOpenAI(
        model=settings.OPENAI_CHAT_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )


def query_rag(
    rag_request: RagRequest,
    user_id: int,
) -> RagResponse:
    question = rag_request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    top_k = max(
        1,
        min(rag_request.top_k or 5, 20),
    )

    # Retrieval happens before LLM creation.
    # This allows an empty document collection to return
    # the correct "I don't know" response without an API key.
    try:
        results = similarity_search(
            query=question,
            user_id=user_id,
            k=top_k,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document retrieval failed: {exc}",
        ) from exc

    if not results:
        return RagResponse(
            answer="I don't know based on the uploaded documents.",
            sources=[],
        )

    # Only create the LLM when documents were actually retrieved.
    llm = _get_llm()

    context_parts = []
    sources = []

    for document, score in results:
        metadata = document.metadata or {}

        document_id = metadata.get("document_id")
        filename = metadata.get("filename", "Unknown")
        page_number = metadata.get("page_number", "Unknown")

        context_parts.append(
            f"Document: {filename}\n"
            f"Page: {page_number}\n"
            f"Content:\n{document.page_content}"
        )

        sources.append(
            {
                "id": document_id,
                "filename": filename,
                "page_number": page_number,
                "content": document.page_content,
                "score": float(score),
            }
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an enterprise document assistant.

Answer the user's question ONLY using the supplied document context.

Rules:
- Do not invent facts.
- If the answer is not present in the context, say you don't know.
- Use only information supported by the context.
- Mention the relevant document filename and page when appropriate.
- Keep the answer clear and concise.

Document context:

{context}
""",
            ),
            (
                "human",
                "{question}",
            ),
        ]
    )

    try:
        messages = prompt.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = llm.invoke(messages)

        return RagResponse(
            answer=str(response.content),
            sources=sources,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG generation failed: {exc}",
        ) from exc
