from app.vectorstore.chroma_client import collection
from app.ai.embeddings import get_embedding

def retrieve_relevant_knowledge(query: str, top_k: int = 3) -> str:
    """Retrieve top_k relevant documents from vector DB."""
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    documents = results['documents'][0]
    return "\n\n".join(documents)