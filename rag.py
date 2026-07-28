import os
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_SAVE_PATH = "faiss_index"

_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(INDEX_SAVE_PATH):
    _vector_store = FAISS.load_local(
        INDEX_SAVE_PATH, 
        _embeddings, 
        allow_dangerous_deserialization=True
    )
else:
    _vector_store = None


@tool
def search_health_knowledge_base(query: str) -> str:
    """
    Searches the verified health and safety knowledge base for guidance on exercise safety,
    injury signs, DOMS vs acute injury, overtraining, chest pain, sleep, hydration, and medical disclaimers.
    Always call this tool when the user asks a health, medical, safety, or physical injury question.
    """
    if _vector_store is None:
        return "Knowledge base index is not available. Please run build_kb.py first."

    docs = _vector_store.similarity_search(query, k=3)
    if not docs:
        return "No relevant health or safety information found in the knowledge base."

    formatted_results = []
    for i, doc in enumerate(docs, 1):
        formatted_results.append(f"--- Passage {i} ---\n{doc.page_content}")

    return "\n\n".join(formatted_results)