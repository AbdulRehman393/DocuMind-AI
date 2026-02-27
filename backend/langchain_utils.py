from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from chroma_utils import vectorstore
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

@tool
def document_search(q):
    """Searches your uploaded documents and returns relevant content."""
    docs = retriever.invoke(q)
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def web_search(q):
    """Live search for current events, weather, or today's date."""
    print(f"web_search called with: {q}")
    wrapper = SerpAPIWrapper()
    return wrapper.run(q)

from langchain.agents import initialize_agent, AgentType

GREETINGS = ["hi", "hello", "hey", "salaam", "assalam", "good morning", "good afternoon", "good evening"]
def is_greeting(msg):
    norm = msg.lower().strip()
    return any(g in norm for g in GREETINGS)

def get_rag_chain(model="nvidia/nemotron-nano-9b-v2:free"):
    llm = ChatOpenAI(
        model=model,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    class AgentRAGChain:
        def invoke(self, inputs):
            user_q = inputs["input"]
            normalized_q = user_q.lower().strip()

            print("User asked:", user_q)

            if is_greeting(normalized_q) or normalized_q in ["how are you?", "what's up?", "are you there?"]:
                return {"answer": "Hello! How can I assist you today?"}

            if any(kw in normalized_q for kw in ["date", "weather", "today", "now", "current", "temperature"]):
                tool_data = web_search(user_q)
                prompt = (
                    f"You are a helpful assistant. The user asked: '{user_q}'.\n"
                    f"Here is info from a web tool: {tool_data}\n"
                    "Reply with one clear, friendly, human sentence answering only what the user asked."
                )
                try:
                    llm_result = llm.invoke(prompt)
                    content = getattr(llm_result, 'content', None) or str(llm_result)
                    return {"answer": content.strip()}
                except Exception as e:
                    print(f"Web LLM error: {e}")
                    return {"answer": str(tool_data)}

            # Try doc (vectorstore) last (if not a live-data question)
            print("Trying PDF/doc search...")
            doc_answer = document_search(user_q)
            print("Doc search result:", doc_answer)

            if doc_answer and doc_answer.strip():
                check_prompt = (
                    f"You are a helpful document assistant. User asked: '{user_q}'\n"
                    f"Found in documents: '''{doc_answer}'''\n"
                    "If this really answers the user's question, reply with a friendly, concise answer. "
                    "If NOT, reply ONLY with: NOT FOUND."
                )
                try:
                    llm_result = llm.invoke(check_prompt)
                    content = getattr(llm_result, 'content', None) or str(llm_result)
                    print("Doc LLM result:", content)
                    if "NOT FOUND" not in content.upper():
                        return {"answer": content.strip()}
                except Exception as e:
                    print(f"PDF LLM check failed: {e}")

            # Try pure LLM last
            print("Trying direct LLM fallback...")
            try:
                result = llm.invoke(user_q)
                content = getattr(result, 'content', None) or str(result)
                print("Direct LLM result:", content)
                return {"answer": content.strip()}
            except Exception as e:
                print(f"Agent fallback error: {e}")
                return {"answer": f"Sorry, something went wrong: {e}"}
    return AgentRAGChain()