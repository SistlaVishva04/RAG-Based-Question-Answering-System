from app.services.vector_service import VectorService
from app.services.llm_service import LLMService

class RAGService:
    def __init__(self):
        self.vector_service = VectorService()
        self.llm = LLMService()

    def chat(self, document_id: str, query: str) -> str:
        chunks = self.vector_service.similarity_search(
            query=query,
            document_id=document_id
        )

        if not chunks:
            return "No relevant content found in the document."

        context = "\n\n".join([c["text"] for c in chunks])

        return self.llm.generate_answer(context, query)
