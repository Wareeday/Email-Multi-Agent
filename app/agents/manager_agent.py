from app.ai.llm import get_llm
from app.ai.prompts import MANAGER_CLASSIFICATION_PROMPT
from app.services.sentiment_service import analyze_sentiment
import json

class ManagerAgent:
    def __init__(self):
        self.llm = get_llm()

    async def classify(self, email_subject: str, email_body: str, sentiment_score: float) -> str:
        """Classify email into support, sales, or escalation."""
        prompt = MANAGER_CLASSIFICATION_PROMPT.format(
            subject=email_subject,
            body=email_body,
            sentiment=sentiment_score
        )
        response = await self.llm.acomplete(prompt)
        # Expect response like: {"intent": "support", "reason": "..."}
        try:
            result = json.loads(response)
            return result.get("intent", "support")
        except:
            # Fallback
            return "support"