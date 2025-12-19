from sentence_transformers import SentenceTransformer
from vectorstore.vectordb import similarity_search

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_query(text: str):
    embedding = model.encode([text]).tolist()[0]
    return embedding

def get_similarity_search(text: str, top_k: int = 5):
    query_embedding = embed_query(text)
    results = similarity_search(query_embedding, top_k=top_k)
    return results
