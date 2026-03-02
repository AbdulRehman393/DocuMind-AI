import streamlit as st
import uuid
import time
from sidebar import render_sidebar
from api_utils import send_chat_message

st.set_page_config(
    page_title="DocuMind Nexus",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session state ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar returns selected model + UI toggles
model, show_details = render_sidebar()

# ---------- Header ----------
st.title("DocuMind Nexus")
st.caption("Docs-first RAG assistant with live web search fallback (SerpAPI).")

# ---------- Top bar ----------
c1, c2, c3, c4 = st.columns([1.2, 2.6, 1.8, 2.0], vertical_alignment="center")
with c1:
    st.success("Online")
with c2:
    st.metric("Model", model.split("/")[-1])
with c3:
    st.metric("Session", st.session_state.session_id[:8])
with c4:
    if st.button("New conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

st.divider()

# ---------- ONE Chat Panel (no duplication) ----------
with st.container(border=True):
    st.subheader("Chat")

    # Empty state
    if not st.session_state.messages:
        st.info("Upload a document from the sidebar, then ask questions. For weather/news, just ask normally.")

    # Render chat history (ONLY here)
    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🧠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

            if show_details and msg["role"] == "assistant":
                meta = msg.get("meta", {}) or {}
                with st.expander("Details", expanded=False):
                    st.write(f"Model: `{meta.get('model', model)}`")
                    st.write(f"Session: `{(meta.get('session_id') or st.session_state.session_id)[:8]}`")
                    if meta.get("source") is not None:
                        st.write(f"Source: `{meta.get('source')}`")
                    if meta.get("latency_ms") is not None:
                        st.write(f"Latency: `{meta.get('latency_ms')} ms`")

# Chat input OUTSIDE container (Streamlit best behavior)
prompt = st.chat_input("Ask anything about your documents (or ask about weather/news)...")
if prompt:
    # Append user msg
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call backend
    with st.chat_message("assistant", avatar="🧠"):
        start = time.perf_counter()
        with st.spinner("Thinking..."):
            try:
                response = send_chat_message(prompt, model, st.session_state.session_id)
                latency_ms = int((time.perf_counter() - start) * 1000)

                if response.status_code == 200:
                    payload = response.json()

                    returned_session_id = payload.get("session_id")
                    if returned_session_id:
                        st.session_state.session_id = returned_session_id

                    answer = payload.get("answer", "No response received.")
                    source = payload.get("source")

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "meta": {
                            "model": model,
                            "session_id": st.session_state.session_id,
                            "source": source,
                            "latency_ms": latency_ms,
                        }
                    })
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Cannot connect to backend: {e}")

    # Rerun so the user message + assistant message appear in the panel above immediately
    st.rerun() 