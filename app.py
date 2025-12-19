from dotenv import load_dotenv
load_dotenv()   

from fastapi import FastAPI, UploadFile, File, Form,Request
from fastapi.middleware.cors import CORSMiddleware
from chat.chat_manager import ChatManager
from multimodal.image_generation import generate_image
from fastapi.responses import StreamingResponse
import io
import base64
from ingestion.ingestor import ingest_image_file, ingest_text_document
import os

app = FastAPI()
chat_manager = ChatManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "Multimodal Chatbot API Running"}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename

    dest = os.path.join(
        "storage",
        "images" if file.content_type.startswith("image/") else "uploads",
        filename
    )
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(dest, "wb") as f:
        f.write(content)

    if file.content_type.startswith("image/"):
        caption = analyze_image_bytes(content)
        result = ingest_image_file(dest, caption)
        return {"status": "image_ingested", "caption": caption, "result": result}
    else:
        try:
            text = content.decode("utf-8")
            with open(dest, "w", encoding="utf-8") as f:
                f.write(text)
            result = ingest_text_document(dest)
            return {"status": "text_ingested", "result": result}
        except:
            return {"status": "unknown_file_type"}

@app.post("/multimodal_chat")
async def multimodal_chat(query: str = Form(...), image: UploadFile | None = File(None)):
    extra = ""
    if image:
        b = await image.read()
        caption = analyze_image_bytes(b)
        extra = f"Image caption: {caption}"
    answer = chat_manager.query(query, extra_context=extra)
    return {"answer": answer}



@app.post("/generate_image")
async def generate_image_endpoint(prompt: str = Form(...)):
    print("Generating image with OpenAI DALL·E...")

    from multimodal.image_generation import generate_image
    img_bytes = generate_image(prompt)  # returns BASE64 string

    # Convert base64 → PNG stream
    png_data = base64.b64decode(img_bytes)

    return StreamingResponse(
        io.BytesIO(png_data),
        media_type="image/png"
    )

   

