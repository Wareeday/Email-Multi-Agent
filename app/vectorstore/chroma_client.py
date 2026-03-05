import chromadb
from chromadb.config import Settings
from app.ai.embeddings import get_embedding
from app.utils.logger import logger
import os

# Initialize persistent Chroma client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection_name = "knowledge_base"
collection = client.get_or_create_collection(
    name=collection_name,
    embedding_function=None  # We'll provide embeddings manually
)

def load_knowledge_base(folder_path: str):
    """Load all markdown files from folder into vector DB."""
    documents = []
    metadatas = []
    ids = []
    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".md"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r") as f:
                content = f.read()
            documents.append(content)
            metadatas.append({"source": filename})
            ids.append(f"doc_{idx}")

    # Generate embeddings
    embeddings = [get_embedding(doc) for doc in documents]

    # Add to collection
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    logger.info(f"Loaded {len(documents)} documents into vector DB.")

# If run directly, load knowledge base
if __name__ == "__main__":
    load_knowledge_base("./knowledge_base")