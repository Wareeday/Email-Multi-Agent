from openai import AsyncOpenAI
from app.config.settings import settings

class LLM:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"  # or "gpt-3.5-turbo"

    async def acomplete(self, prompt: str, max_tokens: int = 500) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

# Singleton
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLM()
    return _llm_instance