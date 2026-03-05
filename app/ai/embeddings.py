from openai import OpenAI
from app.config.settings import settings

client = OpenAI(api_key=settings.openai_api_key)

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding