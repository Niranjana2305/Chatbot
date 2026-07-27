import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

INDEX_SAVE_PATH = "faiss_index"

def build_vector_store():
    print("loading documents from knowledge base...")
    loader = DirectoryLoader(
        path="knowledge_base",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from knowledge base.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=70,
        length_function=len,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    print("Splitting documents into chunks...")
    chunks = text_splitter.split_documents(docs)
    print(f"Split {len(chunks)} chunks from {len(docs)} documents.")

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    print(f"Loading embedding model: {model_name}...")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print(f"Loaded embedding model: {model_name}.")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("FAISS vector store built successfully.")

    vectorstore.save_local(INDEX_SAVE_PATH)
    print(f"FAISS index saved successfully to '{INDEX_SAVE_PATH}' directory!")

if __name__ == "__main__":
    build_vector_store()