import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from app.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(
            name="parcelpilot_docs",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Dict[str, Any]]):
        ids = [f"doc_{i}_{doc['metadata']['source']}_p{doc['metadata']['page']}" for i, doc in enumerate(documents)]
        texts = [doc["text"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )

    def search(self, query: str, n_results: int = 4, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        kwargs = {
            "query_texts": [query],
            "n_results": n_results
        }
        if filters:
            kwargs["where"] = filters

        results = self.collection.query(**kwargs)
        
        formatted = []
        if results and results.get("documents") and results["documents"][0]:
            for text, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
                formatted.append({
                    "content": text,
                    "metadata": meta,
                    "similarity": round(1.0 - dist, 4)
                })
        return formatted