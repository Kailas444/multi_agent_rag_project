import os
from typing import List
from pypdf import PdfReader
from langchain_core.documents import Document

def extract_pdf_pages(path: str) -> List[Document]:
    reader = PdfReader(path)
    docs = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": os.path.basename(path), "page": i}
                )
            )
    return docs
