# RAG Chatbot (FastAPI + Streamlit + LangChain + Chroma)

> **Status: Work in Progress (WIP)** — this project is actively being developed and may change frequently.

A simple Retrieval-Augmented Generation (RAG) chatbot that lets you upload documents (PDF/TXT/MD), indexes them into a Chroma vector database, and then answers questions using retrieved context.

## Features
- Upload and ingest: **PDF, TXT, MD**
- Text chunking with `RecursiveCharacterTextSplitter`
- Vector storage with **Chroma (persistent)**
- Chat UI with **Streamlit**
- RAG answering with **LangChain** and an OpenAI-compatible chat model (configured for **OpenRouter**)

---

## Tech Stack
- Backend API: **FastAPI**
- Frontend: **Streamlit**
- RAG: **LangChain**
- Vector DB: **Chroma**
- Embeddings: `OpenAIEmbeddings` (OpenAI-compatible)
- LLM: `ChatOpenAI` (OpenAI-compatible, configured for OpenRouter)

---

## Project Structure
```text
rag-chatbot/
├─ main.py                  # FastAPI app (ingest + chat endpoints)
├─ app.py                   # Streamlit UI
└─ app/
   └─ rag/
      ├─ ingest.py          # loaders + chunking + ingestion
      ├─ chat.py            # RAG chain (retriever + prompt + LLM)
      └─ vectorstore.py     # Chroma vectorstore setup
```

---

## Setup

### 1) Create and activate a virtual environment
Windows (PowerShell):
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt` yet, install the core packages:
```bash
pip install fastapi uvicorn streamlit python-dotenv requests chromadb \
  langchain langchain-community langchain-openai langchain-text-splitters pypdf
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
# Backend API
API_URL=http://127.0.0.1:8000

# OpenRouter (for chat model)
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini

# (Optional) OpenAI key if you use OpenAI embeddings directly
OPENAI_API_KEY=your_openai_key_here

# Optional default model name used by UI
OPENAI_MODEL=gpt-4o-mini
```

> Tip: never commit your real `.env` to GitHub.

---

## Run the Backend (FastAPI)
```bash
uvicorn main:app --reload --port 8000
```

API endpoints:
- `POST /ingest` (file upload)
- `POST /chat` (ask question)

---

## Run the Frontend (Streamlit)
In a new terminal:
```bash
streamlit run app.py
```

---

## Usage
1. Open Streamlit UI
2. Upload a file (PDF/TXT/MD) and click **Index file**
3. Ask questions about your uploaded documents

---

## Notes / Troubleshooting
- Chroma data persists under: `data/chroma/`
- If ingestion fails, check that your embeddings provider API key is set.
- If answers are "I don't know", try ingesting the file again or uploading a more text-readable PDF.

---

## License
MIT (or choose your preferred license).
