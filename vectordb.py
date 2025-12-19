import chromadb
import os

DB_FOLDER = "db"


if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)


client = chromadb.PersistentClient(path=DB_FOLDER)


collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}   # cosine similarity
)

def add_embeddings(embeddings, chunks):
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=[{"text": chunk} for chunk in chunks]
    )

def similarity_search(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )


    if results["metadatas"]:
        return [meta["text"] for meta in results["metadatas"][0]]

    return []
