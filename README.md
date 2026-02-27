# DocuMind AI
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Repo](https://img.shields.io/badge/repo-DocuMind--AI-purple)](https://github.com/AbdulRehman393/DocuMind-AI)

🧠 DocuMind AI — Your intelligent document assistant. Upload PDF, DOCX or HTML files, index them, and ask questions in natural language to get accurate, context-aware answers powered by a lightweight RAG pipeline.

---

## ✨ Highlights
- Upload and index documents (PDF/DOCX/HTML).
- Retrieval-Augmented Generation (RAG) chat powered by LangChain + Chroma.
- Lightweight, offline-friendly embeddings (SimpleHashEmbeddings) for demo/local use.
- Modern Streamlit UI with model selector and sessions.
- FastAPI backend that handles document processing, indexing, chat, and document management.

---

## 🧭 Demo
Add a screenshot here to showcase the UI:
```
/images/project.png
```
(Replace with your production screenshot or link for the README preview)

---

## 🚀 What's New / Improvements
- Streamlined front-end (Streamlit) UI with improved styling and model selector.
- Added offline-friendly SimpleHashEmbeddings so the demo works without external embedding APIs.
- Robust FastAPI backend with endpoints for uploading, listing, deleting documents and chat queries.
- LangChain integration for retriever + tools (document_search, web_search) and agent orchestration.
- Better session handling and chat history support in the frontend.

---

## Features
- Multi-format document support (PDF, DOCX, HTML)
- Fast local indexing with text-splitting and Chroma vector DB
- Chat interface with session history
- Model selector for trying different LLM backends (plug-and-play)
- Simple, secure `.env` driven configuration
- Offline demo mode (no external API required) via hash-embeddings

---

## 📁 Project Structure
- `backend/` — FastAPI app, LangChain utilities, Chroma integration, and DB helpers.
- `frontend/` — Streamlit app, sidebar, API helpers, and UI assets.
- `.env.example` — Example environment variables (copy to `.env`).
- `requirements.txt` — Python dependencies required for both frontend and backend.
- `README.md` — This file.
- `LICENSE` — Project license (MIT).

---

## ⚡ Quick Start (Local)
1. Clone the repo
```bash
git clone https://github.com/AbdulRehman393/DocuMind-AI.git
cd DocuMind-AI
```

2. Create & activate virtual environment
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Copy env example and edit
```bash
cp .env.example .env
# Edit `.env` to configure keys or settings. For offline demo, many keys are optional.
```

5. Run backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. Run frontend (in a separate terminal)
```bash
cd frontend
streamlit run streamlit_app.py
# or if your main file is named `app.py`: streamlit run app.py
```

7. Open the app
- Streamlit: http://localhost:8501
- Backend API: http://localhost:8000/docs (FastAPI interactive docs)

---

## ⚙️ Environment Variables (suggested)
See `.env.example` in the repo — copy it to `.env` and configure as needed. Typical variables:
- OPENROUTER_API_KEY / OPENAI_API_KEY — (optional) LLM provider API key if you want to use a hosted model.
- CHROMA_DB_DIR — (optional) directory path to persist Chroma DB.
- BACKEND_PORT — (optional) port number for the FastAPI backend.
Notes:
- For offline demo/testing you can omit LLM provider keys and rely on local mock/agent configs in the repo (SimpleHashEmbeddings + default model selection).

---

## 🧠 How it works (high level)
1. Upload a document via the Streamlit sidebar.
2. Backend parses the document (PDF/DOCX/HTML), splits text into chunks, and creates embeddings (SimpleHashEmbeddings by default).
3. Chroma stores vectors and provides a retriever to fetch relevant chunks.
4. LangChain RAG chain constructs context and sends it to the selected model (local or hosted) to generate an answer.
5. Chat history and documents are listed in the UI; documents can be removed from Chroma and database.

---

## API Endpoints (summary)
- POST `/upload-doc` — Uploads and indexes a document.
- GET `/list-docs` — Lists indexed documents.
- POST `/delete-doc` — Delete a document by id.
- POST `/chat` — Send a question, returns a response object with answer and metadata.

(Use http://localhost:8000/docs for interactive OpenAPI docs.)

---

## Usage Tips
- Use the model selector in the sidebar to experiment with different LLM backends.
- For large PDFs, allow a few seconds for indexing.
- If the backend is offline, the frontend shows an informative message and instructions to launch the backend.

---

## Troubleshooting
- Backend unreachable: Ensure `uvicorn main:app --reload` is running and `API_URL` in `frontend/api_utils.py` matches.
- File not indexing: Check backend logs (`app.log`) for parsing errors and ensure file types are supported (pdf, docx, html).
- Slow responses: Increase the retriever `k` or tweak chunk sizes in `chroma_utils.py`.

---

## Development
- Code is split into clear modules: `chroma_utils.py` (parsing & vector store), `langchain_utils.py` (chains & tools), `db_utils.py` (document metadata & logs), plus the Streamlit frontend.
- Tests: Add unit tests for parsers and vectorstore logic to `tests/` as the next step.

---

## Contributing
Contributions, issues, and feature requests are welcome!
1. Fork the repo
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit changes and push: `git push origin feature/your-feature`
4. Open a Pull Request describing your changes

Please run formatting and linting (if configured) before submitting PRs.

---

## License
This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

## Author & Contact
Built with ❤️ by [AbdulRehman393](https://github.com/AbdulRehman393).  
For questions or support, open an issue in this repo.

---

Thank you for building DocuMind AI! If you'd like, I can:
- Add a ready-to-use GitHub Actions workflow for testing & linting,
- Generate a production-ready Dockerfile + docker-compose for easy deployment,
- Or update `.env.example` with exact env keys found in the codebase.

Tell me which of these you'd like next and I’ll prepare the files.
