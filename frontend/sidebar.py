import streamlit as st
import uuid
from api_utils import upload_document, get_all_documents, delete_document

def render_sidebar():
    st.sidebar.title("DocuMind Nexus")
    st.sidebar.caption("Docs-first RAG + live web search")

    # Small status box (professional feel)
    with st.sidebar.container(border=True):
        st.write("Status: **Online**")
        st.write("Mode: **Docs → Web**")

    tab_upload, tab_docs, tab_settings = st.sidebar.tabs(["Upload", "Documents", "Settings"])

    # ===== Upload =====
    with tab_upload:
        with st.sidebar.container(border=True):
            st.subheader("Upload & Index")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["pdf", "docx", "html"],
                help="Upload a document to index into the vector database for RAG.",
            )

            if st.button("Upload & index", use_container_width=True, disabled=uploaded_file is None):
                with st.status("Indexing document...", expanded=True) as status:
                    try:
                        response = upload_document(uploaded_file)
                        if response.status_code == 200:
                            status.update(label="Indexed successfully", state="complete")
                            st.success(f"Indexed: {uploaded_file.name}")
                        else:
                            status.update(label="Indexing failed", state="error")
                            st.error(response.text)
                    except Exception as e:
                        status.update(label="Upload failed", state="error")
                        st.error(str(e))

        with st.sidebar.expander("Tips"):
            st.write("• Upload PDF/DOCX/HTML and ask questions from chat.")
            st.write("• Weather/news/latest questions use web search automatically.")

    # ===== Documents =====
    with tab_docs:
        with st.sidebar.container(border=True):
            st.subheader("Indexed documents")
            documents = get_all_documents()

            if documents is None:
                st.warning("Backend offline. Start FastAPI server first (python main.py).")
            elif not documents:
                st.info("No documents yet. Upload one from the Upload tab.")
            else:
                for doc in documents:
                    col1, col2 = st.columns([6, 1], vertical_alignment="center")
                    with col1:
                        st.write(f"📄 {doc['filename']}")
                    with col2:
                        if st.button("Delete", key=f"del_{doc['id']}"):
                            resp = delete_document(doc["id"])
                            if resp.status_code == 200:
                                st.success("Deleted")
                                st.rerun()
                            else:
                                st.error(resp.text)

    # ===== Settings =====
    with tab_settings:
        with st.sidebar.container(border=True):
            st.subheader("AI Model")
            model = st.selectbox(
                "Select model",
                [
                    "nvidia/nemotron-nano-9b-v2:free",
                    "qwen/qwen3-4b:free",
                    "deepseek/deepseek-r1-0528:free",
                    "mistralai/mistral-small-3.1-24b-instruct:free",
                ],
                index=0,
            )

        with st.sidebar.container(border=True):
            st.subheader("UI")
            show_details = st.toggle(
                "Show answer details (model/session/source)",
                value=False,
            )

        with st.sidebar.container(border=True):
            st.subheader("Conversation")
            if st.button("New conversation", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.rerun()

        with st.sidebar.container(border=True):
            st.subheader("About")
            st.caption("Streamlit + FastAPI + LangChain + Chroma + OpenRouter + SerpAPI")

    st.sidebar.divider()
    st.sidebar.caption("Built by Abdul Rehman")

    return model, show_details