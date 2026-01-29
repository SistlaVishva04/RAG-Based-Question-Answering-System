from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class VectorService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.Client(
            Settings(
                persist_directory="app/db/vector_store/chroma",
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_chunks(self, document_id: str, chunks: list[str]):

        embeddings = self.model.encode(chunks).tolist()
        ids = [f"{document_id}_{i}" for i in range(len(chunks))]

    # Remove old chunks if re-uploaded
        try:
            existing = self.collection.get(where={"document_id": document_id})
            if existing["ids"]:
                self.collection.delete(ids=existing["ids"])
        except:
            pass

        self.collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"document_id": document_id}] * len(chunks)
    )


        

    def similarity_search(
        self,
        query: str,
        document_id: str,
        top_k: int = 3
    ):
        query_embedding = self.model.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where={"document_id": document_id}
        )

        print("QUERY DOC ID:", document_id)
        print("RAW RESULTS:", results)

        if not results.get("documents") or not results["documents"][0]:
            return []

        return [
            {"text": doc}
            for doc in results["documents"][0]
        ]
