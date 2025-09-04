from google import genai
from PIL import Image
import io
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=gemini_api_key)

def get_llm_response(image_data: bytes) -> str:
    image = Image.open(io.BytesIO(image_data))
    # implement the call to the Gemini API here
    # https://ai.google.dev/gemini-api/docs/text-generation
# Convert PIL image to bytes (PNG format) for Gemini input
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    image_bytes = buf.read()

    # Call Gemini API
    response = gemini_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            {"role": "user", "parts": [
                {"text": "Describe this image in a short caption."},
                {"inline_data": {"mime_type": "image/png", "data": image_bytes}}
            ]}
        ]
    )

    # Return the generated text
    return response.text if hasattr(response, "text") else str(response)

