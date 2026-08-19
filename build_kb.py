import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings

load_dotenv()

INDEX_SAVE_PATH = "faiss_index"
KNOWLEDGE_BASE_DIR = Path("knowledge_base")

def build_vector_store():
    print("Loading documents from knowledge base...")
    
    docs = []
    for file_path in KNOWLEDGE_BASE_DIR.rglob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8")
            docs.append(Document(page_content=content, metadata={"source": str(file_path)}))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    print(f"Loaded {len(docs)} documents from knowledge base.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    print("Splitting documents into chunks...")
    chunks = text_splitter.split_documents(docs)
    print(f"Split {len(chunks)} chunks from {len(docs)} documents.")

    print("Loading ONNX embedding model (FastEmbed)...")
    embeddings = FastEmbedEmbeddings()
    print("Loaded FastEmbed embedding model.")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("FAISS vector store built successfully.")

    vectorstore.save_local(INDEX_SAVE_PATH)
    print(f"FAISS index saved successfully to '{INDEX_SAVE_PATH}' directory!")

if __name__ == "__main__":
    build_vector_store()
