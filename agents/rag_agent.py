import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface import HuggingFacePipeline

def extract_pdf_pages(path):
    reader = PdfReader(path)
    docs = []
    for i, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if text:
            docs.append(Document(
                page_content=text,
                metadata={"source": os.path.basename(path), "page": i}
            ))
    return docs

def initialize_vector_store(pdf_path, faiss_directory, embedding_model):
    os.makedirs(faiss_directory, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    if os.path.exists(os.path.join(faiss_directory, "index.faiss")):
        return FAISS.load_local(
            faiss_directory,
            embeddings,
            allow_dangerous_deserialization=True
        )

    docs = extract_pdf_pages(pdf_path)
    splitter = RecursiveCharacterTextSplitter(500, 100)
    chunks = splitter.split_documents(docs)

    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(faiss_directory)
    return vs

def retrieve_chunks(vector_store, query, k=3):
    docs = vector_store.similarity_search(query, k=k)
    context = "\n\n".join(
        f"(source={d.metadata['source']}, page={d.metadata['page']})\n{d.page_content}"
        for d in docs
    )
    citations = [
        {"source": d.metadata["source"], "page": d.metadata["page"]}
        for d in docs
    ]
    return context, citations

def create_local_llm(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_new_tokens=220)
    return HuggingFacePipeline(pipeline=pipe)

def generate_answer(llm, context, query):
    prompt = f"""
Answer strictly using the context below.
If not found, say "I don't know from the provided documents."

Context:
{context}

Question: {query}
Answer:
"""
    return llm.invoke(prompt)
