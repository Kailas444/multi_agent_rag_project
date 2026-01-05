import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.pdf_loader import extract_pdf_pages

def load_vector_store(
    pdf_path: str,
    faiss_dir: str = "faiss_store",
):
    os.makedirs(faiss_dir, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(os.path.join(faiss_dir, "index.faiss")):
        return FAISS.load_local(
            faiss_dir,
            embeddings,
            allow_dangerous_deserialization=True,
        )

    docs = extract_pdf_pages(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(docs)

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(faiss_dir)

    return vector_store
