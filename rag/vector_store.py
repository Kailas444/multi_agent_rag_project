import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.pdf_loader import extract_pdf_pages

FAISS_DIR = "faiss_store"
PDF_PATH = "data/artificial_intelligence_tutorial.pdf"

_vector_store = None   # 👈 cache (lazy)

def get_vector_store():
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    os.makedirs(FAISS_DIR, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(os.path.join(FAISS_DIR, "index.faiss")):
        _vector_store = FAISS.load_local(
            FAISS_DIR,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        return _vector_store

    docs = extract_pdf_pages(PDF_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(docs)

    _vector_store = FAISS.from_documents(chunks, embeddings)
    _vector_store.save_local(FAISS_DIR)

    return _vector_store
