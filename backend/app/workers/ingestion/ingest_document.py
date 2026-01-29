from app.utils.parsers.pdf_parser import parse_pdf
from app.utils.parsers.txt_parser import parse_txt
from app.utils.chunkers.text_chunker import chunk_text
from app.services.vector_service import VectorService
from app.state.ingestion_state import INGESTION_STATUS




def ingest_document(file_path: str, document_id: str):

    try:
        if file_path.endswith(".pdf"):


            text = parse_pdf(file_path)
        elif file_path.endswith(".txt"):
                
                text = parse_txt(file_path)
        else: 
            return

        chunks = chunk_text(text)

        vector_service = VectorService()
        vector_service.add_chunks(document_id, chunks)
        INGESTION_STATUS[document_id] = "completed"
        print("INGESTION COMPLETED:", document_id)

    except Exception as e:
        INGESTION_STATUS[document_id] = "failed"

        print("INGESTION FAILED:", document_id, e)

