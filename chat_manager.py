# ChatBot/chat/chat_manager.py
from multimodal.embeddings import embed_text
from vectorstore.chroma_store import similarity_search
from .llm import generate_answer

class ChatManager:
    def __init__(self):
        pass

    def query(self, user_query: str, extra_context: str = ""):
        """
        Query can include optional extra_context (for example, image captions).
        """
        # embed the query
        q_emb = embed_text(user_query)
        hits = similarity_search(q_emb, top_k=5)
        # collect hit texts
        contexts = [h["text"] for h in hits]
        combined = "\n\n".join([extra_context] + contexts) if extra_context else "\n\n".join(contexts)
        prompt = f"""You are an assistant that uses the provided context to answer.
Context:
{combined}

Question: {user_query}
Answer concisely and cite relevant context."""
        return generate_answer(prompt)
