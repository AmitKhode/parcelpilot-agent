import os
import pypdf
from typing import List, Dict, Any
from app.config import settings
from app.retrieval.vector_store import VectorStore

METADATA_REGISTRY = {
    "01_Support_Policy_v3_CURRENT.pdf": {
        "version": "v3",
        "status": "CURRENT",
        "authority": 2,
        "type": "General Policy",
        "effective_date": "2026-05-01"
    },
    "02_Support_Policy_v2_DEPRECATED.pdf": {
        "version": "v2",
        "status": "DEPRECATED",
        "authority": 5,
        "type": "General Policy",
        "effective_date": "2025-01-01"
    },
    "03_Cancellation_and_Service_Credit_SOP_v4.pdf": {
        "version": "v4",
        "status": "CURRENT",
        "authority": 2,
        "type": "SOP",
        "effective_date": "2026-06-15"
    },
    "04_Product_Operations_Guide_and_Known_Issues.pdf": {
        "version": "v1",
        "status": "CURRENT",
        "authority": 3,
        "type": "Product Operations",
        "effective_date": "2026-08-14"
    },
    "05_Northstar_Logistics_Enterprise_Agreement.pdf": {
        "version": "v1",
        "status": "ACTIVE",
        "account_id": "ACCT-001",
        "customer": "Northstar Logistics",
        "authority": 1,
        "type": "Customer Agreement",
        "effective_date": "2026-01-01"
    },
    "06_LumenWorks_Service_Agreement.pdf": {
        "version": "v1",
        "status": "ACTIVE",
        "account_id": "ACCT-002",
        "customer": "LumenWorks",
        "authority": 1,
        "type": "Customer Agreement",
        "effective_date": "2026-03-01"
    }
}

def extract_pdf_chunks(pdf_path: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
    filename = os.path.basename(pdf_path)
    meta = METADATA_REGISTRY.get(filename, {"status": "UNKNOWN", "authority": 4})
    
    chunks = []
    reader = pypdf.PdfReader(pdf_path)
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        words = text.split()
        for i in range(0, max(1, len(words)), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "source": filename,
                        "page": page_idx + 1,
                        **meta
                    }
                })
    return chunks

def ingest_all_documents():
    vstore = VectorStore()
    docs_dir = settings.DOCS_DIR
    all_chunks = []
    
    if os.path.exists(docs_dir):
        for fname in os.listdir(docs_dir):
            if fname.endswith(".pdf"):
                full_path = os.path.join(docs_dir, fname)
                chunks = extract_pdf_chunks(full_path)
                all_chunks.extend(chunks)
                
    if all_chunks:
        vstore.add_documents(all_chunks)
        print(f"Successfully ingested {len(all_chunks)} chunks from {len(os.listdir(docs_dir))} documents.")

if __name__ == "__main__":
    ingest_all_documents()