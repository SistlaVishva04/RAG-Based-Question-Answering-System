from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/")
def chat(request: ChatRequest):
    answer = rag_service.chat(
        document_id=request.document_id,
        query=request.query
    )
    print("CHAT DOCUMENT ID:", request.document_id)


    return {"answer": answer}
