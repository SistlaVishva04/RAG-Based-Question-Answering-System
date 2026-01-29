from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    document_id: str = Field(..., description="ID of the uploaded document")
    query: str = Field(..., min_length=1, description="User question")
