# ChatBot/multimodal/image_understanding.py
import base64
from multimodal.genai_client import client, GENAI_AVAILABLE

def analyze_image_bytes(image_bytes: bytes) -> str:
    """
    Return human-readable description of image. Prefer Google GenAI; fallback to OCR or simple note.
    """
    # Try GenAI if available
    if GENAI_AVAILABLE and client is not None:
        try:
            b64 = base64.b64encode(image_bytes).decode("utf-8")
            # Use model.generate_content or similar API — keep robust to SDK differences
            # This is best-effort: if your installed google-genai version uses a different
            # method name adjust accordingly.
            resp = client.models.generate_content(
                model="gemini-proto" ,  # substitute with the correct image-capable model available to you
                image=[{"image_bytes": b64}],
                contents="Describe this image in detail, list visible objects, and provide a 2-sentence summary for indexing."
            )
            # The SDK response object may differ. Try common attributes:
            text = None
            if hasattr(resp, "text"):
                text = resp.text
            elif hasattr(resp, "output") and isinstance(resp.output, list):
                text = " ".join([str(o) for o in resp.output])
            else:
                text = str(resp)
            return text
        except Exception as e:
            # if GenAI fails, continue to fallback
            pass

    # Fallback: try OCR via pytesseract (if installed)
    try:
        from PIL import Image
        import io
        import pytesseract
        img = Image.open(io.BytesIO(image_bytes))
        ocr_text = pytesseract.image_to_string(img).strip()
        if ocr_text:
            return f"OCR text extracted from image:\n{ocr_text}"
    except Exception:
        pass

    # Last resort
    return "No detailed image analysis available. (Enable GOOGLE_API_KEY for GenAI or install pytesseract for OCR.)"
