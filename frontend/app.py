import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG Document Chat",
    page_icon="📄",
    layout="centered"
)

st.title("📄 RAG Document Chatbot")

# -------------------------------
# Session State
# -------------------------------
if "document_id" not in st.session_state:
    st.session_state.document_id = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Upload Section
# -------------------------------
st.header("Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

# Upload ONLY if:
# - file exists
# - file is different from previous upload
if uploaded_file and uploaded_file.name != st.session_state.uploaded_filename:
    with st.spinner("Uploading & processing document..."):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        response = requests.post(
            f"{BACKEND_URL}/documents/upload",
            files=files
        )

        if response.status_code == 200:
            data = response.json()

            st.session_state.document_id = data["document_id"]
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.chat_history = []  # reset chat for new doc

            st.success("✅ Document uploaded successfully!")
            st.code(f"Document ID: {st.session_state.document_id}")
        else:
            st.error("❌ Failed to upload document")

# -------------------------------
# Chat Section
# -------------------------------
st.header("Chat with Document")

if not st.session_state.document_id:
    st.info("Please upload a document to start chatting.")
else:
    status_placeholder = st.empty()

    while True:
        try:
            status_resp = requests.get(
                f"{BACKEND_URL}/documents/status/{st.session_state.document_id}",
                timeout=5
            )

            if status_resp.status_code == 200:
                status = status_resp.json().get("status")
            else:
                status = "unknown"

        except Exception:
            status = "unknown"

        if status == "completed":
            status_placeholder.success("✅ Document indexed successfully!")
            break

        status_placeholder.warning("⏳ Document is still being indexed. Please wait...")
        time.sleep(1)

    # ---- Show chat history ----
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    user_query = st.chat_input("Ask a question about the document")

    if user_query:
        st.session_state.chat_history.append(("user", user_query))
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("Thinking..."):
            payload = {
                "document_id": st.session_state.document_id,
                "query": user_query
            }

            response = requests.post(
                f"{BACKEND_URL}/chat/",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                answer = response.json().get("answer", "")
            else:
                answer = "❌ Error getting response from server."

        st.session_state.chat_history.append(("assistant", answer))
        with st.chat_message("assistant"):
            st.markdown(answer)
