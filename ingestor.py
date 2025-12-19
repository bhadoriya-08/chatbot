# ChatBot/ingestion/ingestor.py
import os
import uuid
from processor.chunker import chunk_text
from multimodal.embeddings import embed_text
from vectorstore.chroma_store import add_items

def ingest_text_document(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text)
    embeddings = [embed_text(c) for c in chunks]
    ids = [str(uuid.uuid4()) for _ in chunks]
    metas = [{"text": c, "source": filepath} for c in chunks]
    add_items(ids, embeddings, metas)
    return {"ids": ids, "chunks": len(chunks)}

def ingest_image_file(filepath: str, caption: str = None):
    # Read file but do NOT embed raw bytes; embed caption or OCR text
    caps = caption or "Image (no caption)"
    emb = embed_text(caps)
    id0 = str(uuid.uuid4())
    add_items([id0], [emb], [{"caption": caps, "image_path": filepath}])
    return {"id": id0, "caption": caps}
