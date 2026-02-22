from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Use OpenRouter if key is available, otherwise fall back to OpenAI directly
openrouter_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key
    )
    EMBED_MODEL = "openai/text-embedding-3-small"
    EMBED_DIM = 1536
else:
    client = OpenAI()
    EMBED_MODEL = "text-embedding-3-small"
    EMBED_DIM = 1536


def embed_texts(texts: list[str]) -> list[list[float]]:
    try:
        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=texts,
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"Error embedding texts: {e}")
        return []
