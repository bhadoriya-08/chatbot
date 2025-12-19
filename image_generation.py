import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str) -> bytes:
    try:
        print("Generating image with OpenAI DALL·E...")

        response = client.images.generate(
            model="gpt-image-1",   # DALL·E 3 successor
            prompt=prompt,
            size="1024x1024"
        )

        # Image is returned as base64
        image_base64 = response.data[0].b64_json
        img_bytes = base64.b64decode(image_base64)
        return img_bytes

    except Exception as e:
        raise RuntimeError(f"OpenAI image generation failed: {e}")
