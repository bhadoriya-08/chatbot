# ChatBot/multimodal/genai_client.py
import os

GENAI_AVAILABLE = False
client = None

try:
    # google-genai SDK
    from google import genai
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
    else:
        # try ADC (service account) if env var not set
        client = genai.Client()
    GENAI_AVAILABLE = True
except Exception:
    # Google GenAI SDK not available or failed to init
    GENAI_AVAILABLE = False
    client = None
