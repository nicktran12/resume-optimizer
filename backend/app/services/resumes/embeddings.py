from google import genai
from google.genai import types

from app.core.config import get_settings

settings = get_settings()
_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def embed_text(text: str) -> list[float]:
    response = _client.models.embed_content(
        model=settings.EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=settings.EMBEDDING_DIMENSIONS),
    )
    return response.embeddings[0].values

def embed_batch(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = _client.models.embed_content(
        model=settings.EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(output_dimensionality=settings.EMBEDDING_DIMENSIONS),
    )
    return [e.values for e in response.embeddings]