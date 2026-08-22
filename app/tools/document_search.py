from typing import Optional, Dict, Any
from app.retrieval.vector_store import VectorStore

vstore = VectorStore()

def search_documents(query: str, filters: Optional[Dict[str, Any]] = None) -> str:
    """Searches current and deprecated policies, SOPs, known issues, and agreements."""
    results = vstore.search(query=query, n_results=4, filters=filters)
    if not results:
        return "No matching documents found in knowledge base."
    
    formatted = []
    for r in results:
        meta = r["metadata"]
        header = f"=== Document: {meta.get('source')} (Status: {meta.get('status')}, Authority Rank: {meta.get('authority')}) ==="
        formatted.append(f"{header}\n{r['content']}\n")
    return "\n\n".join(formatted)