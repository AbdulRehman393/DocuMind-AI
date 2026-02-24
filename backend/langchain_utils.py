from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from chroma_utils import vectorstore

# Load the API key from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


def get_rag_chain(model="nvidia/nemotron-nano-9b-v2:free"):
    llm = ChatOpenAI(
        model=model,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "RAG Chatbot"
        },
        request_timeout=120
    )

    class SimpleRAGChain:
        def invoke(self, inputs):
            question = inputs["input"]
            chat_history = inputs.get("chat_history", [])

            # Get relevant documents
            try:
                docs = retriever.invoke(question)
                context = "\n\n".join([doc.page_content for doc in docs])
            except Exception:
                context = "No documents found."

            # Build chat history string
            history_str = ""
            for msg in chat_history:
                role = msg.get("role", "human")
                content = msg.get("content", "")
                history_str += f"{role}: {content}\n"

            # Single LLM call
            prompt = ChatPromptTemplate.from_messages([
                ("system", 
                 "You are a helpful AI assistant. Use the following context to answer the user's question.\n\n"
                 f"Context: {context}\n\n"
                 f"Chat History:\n{history_str}" if history_str else
                 "You are a helpful AI assistant. Use the following context to answer the user's question.\n\n"
                 f"Context: {context}"
                ),
                ("human", "{input}")
            ])

            chain = prompt | llm | StrOutputParser()
            answer = chain.invoke({"input": question})

            return {"answer": answer}

    return SimpleRAGChain()