import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.pdf_loader import extract_pdf_pages

FAISS_DIR = "faiss_store"
PDF_PATH = "data/artificial_intelligence_tutorial.pdf"

def load_vector_store():
    os.makedirs(FAISS_DIR, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(os.path.join(FAISS_DIR, "index.faiss")):
        return FAISS.load_local(
            FAISS_DIR,
            embeddings,
            allow_dangerous_deserialization=True,
        )

    docs = extract_pdf_pages(PDF_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(docs)

    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(FAISS_DIR)

    return vs

# ✅ CREATE GLOBAL INSTANCE (THIS WAS MISSING)
vector_store = load_vector_store()
