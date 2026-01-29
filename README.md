# 📄 RAG Document Chatbot (FastAPI + Streamlit)
##  📌 Overview

A Retrieval-Augmented Generation (RAG) based document chatbot that allows users to upload documents (PDF/TXT) and chat with them using semantic search and an LLM.
The system performs background ingestion, vector storage, similarity search, and generates grounded answers strictly from the uploaded document.

---

## 🚀 Features

 - 📂 Upload documents (.pdf, .txt)

- 🧩 Chunk documents and generate embeddings

- 🧠 Store embeddings in ChromaDB (local vector store)

- 🔍 Semantic similarity search using Sentence Transformers

- 💬 Chat with documents using Gemini LLM

- ⚙️ Background ingestion with status tracking

- ⏳ Real-time ingestion status polling

- 🚦 Rate limiting for APIs

- 🖥️ Clean Streamlit-based frontend


---
## 🏗️ System Architecture
```
Frontend (Streamlit)
        |
        v
Backend (FastAPI)
  ├── Upload API
  ├── Background Ingestion
  ├── Status API
  ├── Chat API
        |
        v
Vector Store (ChromaDB)
        |
        v
LLM (Gemini 2.5 Flash)
```

---
## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Backend** | FastAPI, Pydantic |
| **Document Processing** | PyMuPDF (PDF), Plain Text Parser |
| **Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Store** | ChromaDB |
| **LLM** | Google Gemini (`google-genai`) |
| **State Management** | In-memory ingestion state |
| **Rate Limiting** | SlowAPI |
| **Environment** | Python 3.10+, Virtualenv |

---

## 📁 Project Structure
```text
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py
│   │       ├── chat.py
│   │       └── health.py
│   ├── services/
│   │   ├── vector_service.py
│   │   ├── rag_service.py
│   │   └── llm_service.py
│   ├── workers/
│   │   └── ingestion/
│   │       └── ingest_document.py
│   ├── state/
│   │   └── ingestion_state.py
│   ├── schemas/
│   │   └── chat.py
│   └── main.py
│
├── app/db/
│   ├── documents/
│   └── vector_store/chroma/
│
├── .env
├── requirements.txt
└── README.md

frontend/
└── app.py
```

---

## 🔄 Application Flow
1️⃣ **Document Upload**

- User uploads a PDF/TXT file via Streamlit

- Backend stores the file and assigns a document_id

- Ingestion starts in the background

2️⃣ **Background Ingestion**

- Extract text from document

- Split text into chunks

- Generate embeddings

- Store chunks in ChromaDB

- Update ingestion status to completed

3️⃣ **Status Polling**

- Frontend polls /documents/status/{document_id}

- Chat UI unlocks only after ingestion completes

4️⃣ **Chat (RAG)**

- User query → embedding

- Similarity search in ChromaDB

- Relevant chunks passed as context to Gemini

- Gemini generates answer only from document context


---

## 📌 API Endpoints
**Upload Document**
```
POST /documents/upload
```

**Response**
```
{
  "document_id": "uuid",
  "status": "ingestion started"
}
```

**Check Ingestion Status**
```
GET /documents/status/{document_id}
```

**Response**
```
{
  "status": "processing | completed"
}
```

**Chat with Document**
```
POST /chat/
```

**Request**
```
{
  "document_id": "uuid",
  "query": "What does this document contain?"
}
```

**Response**
```
{
  "answer": "Answer generated strictly from the document"
}
```

---

## ⚙️ Setup Instructions
1️⃣ **Clone the Repository**
```
git clone https://github.com/SistlaVishva04/RAG-Based-Question-Answering-System/tree/main/backend
cd backend
```

2️⃣ **Create Virtual Environment**
```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

3️⃣ **Install Dependencies**
```
pip install -r requirements.txt
```

4️⃣ **Environment Variables**
Create a .env file:
```
GEMINI_API_KEY=your_gemini_api_key
```

5️⃣ **Run Backend (IMPORTANT)**
```
python -m uvicorn app.main:app
```

⚠️ Do NOT use **--reload**
(Stateful ingestion requires a single process)

6️⃣ **Run Frontend**
```
streamlit run app.py
```

🚦 **Rate Limiting**

- Implemented using SlowAPI

- Protects backend endpoints from abuse


---

## 🛡️ Safety & Hallucination Control

**The LLM is instructed**:
```
“Answer ONLY using the provided context.
If the answer is not present, respond with:
I don’t know based on the document.”
```
This ensures **zero hallucination**.
**🧪 Example Output**

Query
```
What does this file contain?
```

Answer
```
This file contains information about the complexity of algorithms,
their properties, and an example algorithm with pseudocode.
```

✔ Answer grounded in document content.

---

## 🎯 Final Notes

This project demonstrates a production-style RAG pipeline with:

- Proper async ingestion

- Status tracking

- Vector-based retrieval

- LLM grounding

- Frontend-backend integration

---
## 👤 Author
Vishnu Vamsi

Email: vishnuvamsi04@gmail.com
