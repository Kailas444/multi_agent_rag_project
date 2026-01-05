import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from .pdf_loader import extract_pdf_pages

def initialize_vector_store(
    pdf_path: str,
    faiss_directory: str = "./faiss_store",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
):
    os.makedirs(faiss_directory, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    if os.path.exists(os.path.join(faiss_directory, "index.faiss")):
        return FAISS.load_local(
            faiss_directory, embeddings, allow_dangerous_deserialization=True
        )

    docs = extract_pdf_pages(pdf_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(faiss_directory)
    return vs
