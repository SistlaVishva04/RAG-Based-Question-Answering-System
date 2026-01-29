import os
import uuid
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.workers.ingestion.ingest_document import ingest_document

from app.state.ingestion_state import INGESTION_STATUS

UPLOAD_DIR = "app/db/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter()

@router.post("/upload")
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT allowed")

    document_id = str(uuid.uuid4())
    INGESTION_STATUS[document_id] = "processing"

    file_path = f"{UPLOAD_DIR}/{document_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    background_tasks.add_task(
        ingest_document,
        file_path,
        document_id
    )
    print("UPLOAD DOCUMENT ID:", document_id)


    return {
        "document_id": document_id,
        "status": "ingestion started"
    }

@router.get("/status/{document_id}")
def document_status(document_id: str):
    status = INGESTION_STATUS.get(document_id)
    if not status:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"status": status}

