from pathlib import Path
from typing import Iterable

from langchain_chroma import Chroma
from langchain_core.documents import Document as LangChainDocument
from langchain_openai import OpenAIEmbeddings

from backend.app.settings import settings


COLLECTION_NAME = "enterprise_documents"


def _require_api_key() -> None:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")


def get_embeddings() -> OpenAIEmbeddings:
    _require_api_key()

    return OpenAIEmbeddings(
        model=settings.OPENAI_EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )


def get_vector_store() -> Chroma:
    Path(settings.CHROMA_PERSIST_DIRECTORY).mkdir(
        parents=True,
        exist_ok=True,
    )

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        embedding_function=get_embeddings(),
    )


def add_chunks(chunks: Iterable[LangChainDocument]) -> list[str]:
    chunks = list(chunks)

    if not chunks:
        return []

    vector_store = get_vector_store()
    return vector_store.add_documents(chunks)


def delete_document_vectors(document_id: int) -> None:
    vector_store = get_vector_store()

    collection = vector_store._collection

    result = collection.get(
        where={"document_id": document_id}
    )

    ids = result.get("ids", [])

    if ids:
        collection.delete(ids=ids)


def similarity_search(
    query: str,
    user_id: int,
    k: int = 5,
):
    vector_store = get_vector_store()

    return vector_store.similarity_search_with_score(
        query,
        k=k,
        filter={"user_id": user_id},
    )
