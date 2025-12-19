# ChatBot/vectorstore/chroma_store.py
import os
import chromadb

DB_FOLDER = "db"
os.makedirs(DB_FOLDER, exist_ok=True)

client = chromadb.PersistentClient(path=DB_FOLDER)
collection = client.get_or_create_collection(name="multimodal_docs")

def add_items(ids, embeddings, metadatas):
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

def similarity_search(query_embedding, top_k=5):
    if collection.count() == 0:
        return []
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    # results is a dict with 'ids', 'embeddings', 'metadatas' lists
    # return list of metadatas' text field (if present)
    hits = []
    metas = results.get("metadatas", [])
    if metas and isinstance(metas, list) and len(metas) > 0:
        for meta in metas[0]:
            # prefer caption text, fallback to generic 'text'
            text = meta.get("caption") or meta.get("text") or meta.get("content") or ""
            hits.append({"text": text, "meta": meta})
    return hits
