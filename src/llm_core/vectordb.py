# import chromadb
# from typing import Optional, Dict
# import uuid
# from datetime import datetime
# from typing import List

# # Initialize persistent ChromaDB client (make sure chroma DB folder exists or is writable)
# from config import TMP_BASE_PATH
# import os

# TMP_BASE_PATH = "../"
# # Create full path for persistence directory inside TMP_BASE_PATH
# persistence_path = os.path.join(TMP_BASE_PATH, "chroma_db")

# # Ensure the directory exists
# os.makedirs(persistence_path, exist_ok=True)

# # Initialize persistent ChromaDB client with this path
# chroma_client = chromadb.PersistentClient(path=persistence_path)
# def vectordb_store(collection_name: str, file_data: str, metadata: Optional[Dict] = None) -> str:
#     """
#     Store file data in a ChromaDB collection with optional metadata.
    
#     Args:
#         collection_name (str): The name of the collection.
#         file_data (str): The content of the document to be stored.
#         metadata (dict, optional): Optional metadata for the document.

#     Returns:
#         str: The unique ID of the stored document.
#     """
#     # Get or create the collection
#     collection = chroma_client.get_or_create_collection(name=collection_name)
    
#     # Generate a unique ID for the document
#     doc_id = str(uuid.uuid4())
    
#     # Add document to collection
#     collection.add(
#         documents=[file_data],
#         metadatas=[metadata] if metadata else None,
#         ids=[doc_id]
#     )
    
#     return doc_id

# def embed_and_store(file_path: str, file_content: str, collection_name: str = "default") -> str:
#     """
#     Embeds the given content and stores it in the vector database.
#     (Assuming embedding is handled automatically by ChromaDB or external embedder.)
    
#     Args:
#         file_path (str): Identifier for the document (e.g. filename or "combined_files").
#         file_content (str): The content string to embed and store.
#         collection_name (str): Collection name in the vector DB.
    
#     Returns:
#         str: The unique document ID after storing.
#     """
#     metadata = {
#         "file_path": file_path,
#         "source": "combined_embedding",
#         "timestamp": datetime.utcnow().isoformat()
#     }
    
#     doc_id = vectordb_store(collection_name, file_content, metadata)
#     return doc_id


# from sentence_transformers import SentenceTransformer


# # Load embedding model once
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# def retrieve_similar_docs(query: str, collection_name: str = "default", top_k: int = 3) -> List[str]:
#     """
#     Retrieve top-k similar documents from ChromaDB for a given query.

#     Args:
#         query (str): The query string.
#         collection_name (str): The name of the ChromaDB collection.
#         top_k (int): Number of top results to retrieve.

#     Returns:
#         List[str]: A list of top-k document strings.
#     """
#     # Convert the query to embedding
#     query_embedding = embedding_model.encode(query).tolist()

#     # Load the collection
#     collection = chroma_client.get_or_create_collection(name=collection_name)

#     # Query the collection
#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k
#     )

#     # Return document texts (first hit's documents list)
#     return results.get("documents", [[]])[0]



import chromadb
from typing import Optional, Dict
import uuid
from datetime import datetime
from typing import List
import os
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import torch

# Initialize persistent ChromaDB client
TMP_BASE_PATH = "../"
persistence_path = os.path.join(TMP_BASE_PATH, "chroma_db")
os.makedirs(persistence_path, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=persistence_path)

# def vectordb_store(collection_name: str, file_data: str, metadata: Optional[Dict] = None) -> str:
#     """
#     Store file data in a ChromaDB collection with optional metadata.
#     """
#     collection = chroma_client.get_or_create_collection(name=collection_name)
#     doc_id = str(uuid.uuid4())
#     collection.add(
#         documents=[file_data],
#         metadatas=[metadata] if metadata else None,
#         ids=[doc_id]
#     )
#     return doc_id


# def embed_and_store(collection_name: str, file_path: str, file_content: str):
#     metadata = {"path": file_path}
#     vectordb_store(collection_name=collection_name, file_data=file_content, metadata=metadata)

def vectordb_store(collection_name: str, file_data: str, embedding: List[float], metadata: Optional[Dict] = None) -> str:
    """
    Store file data and its embedding in a ChromaDB collection with optional metadata.
    """
    collection = chroma_client.get_or_create_collection(name=collection_name)
    doc_id = str(uuid.uuid4())
    collection.add(
        documents=[file_data],
        embeddings=[embedding],
        metadatas=[metadata] if metadata else None,
        ids=[doc_id]
    )
    return doc_id

def embed_and_store(collection_name: str, file_path: str, file_content: str):
    """
    Embed the content and store it along with metadata in the vector DB.
    """
    metadata = {"path": file_path}
    embedding = embedding_model.encode(file_content, device=device).tolist()
    vectordb_store(
        collection_name=collection_name,
        file_data=file_content,
        embedding=embedding,
        metadata=metadata
    )

# Initialize embedding model with device handling
def get_embedding_model() -> Tuple[SentenceTransformer, str]:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.to(torch.device(device))
    return model, device

embedding_model, device = get_embedding_model()

def retrieve_similar_docs( collection_name: str ,query: str,  top_k: int = 1) -> List[str]:
    """
    Retrieve top-k similar documents from ChromaDB for a given query.
    """
    query_embedding = embedding_model.encode(query, device=device).tolist()

    collection = chroma_client.get_or_create_collection(name=collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results.get("documents", [[]])[0]
