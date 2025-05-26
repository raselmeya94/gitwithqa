# import os
# from sentence_transformers import SentenceTransformer
# from chromadb import PersistentClient
# from config import TMP_BASE_PATH  # your base path from config

# # --- Create vectordb path ---
# VECTORD_DB_PATH = os.path.join(TMP_BASE_PATH, "vectordb")

# # --- VectorDB setup (new client style) ---
# chroma_client = PersistentClient(path=VECTORD_DB_PATH)
# collection = chroma_client.get_or_create_collection(name="my_collection")

# # --- Embedding model load ---
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# def embed_and_store(file_path, file_content):
#     """
#     Given a file path and content, generate embedding and store in vectorDB.
#     """
#     embedding = embedding_model.encode(file_content).tolist()
#     collection.add(
#         documents=[file_content],
#         embeddings=[embedding],
#         metadatas=[{"path": file_path}],
#         ids=[file_path]
#     )
#     print(f"Embedded and stored: {file_path}")
