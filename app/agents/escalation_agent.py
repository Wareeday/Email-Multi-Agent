from app.ai.llm import get_llm
from app.ai.prompts import ESCALATION_REPLY_PROMPT

class EscalationAgent:
    def __init__(self):
        self.llm = get_llm()

    async def generate_reply(self, customer_email: str, conversation_history: str, email_body: str) -> str:
        prompt = ESCALATION_REPLY_PROMPT.format(
            history=conversation_history,
            email_body=email_body
        )
        reply = await self.llm.acomplete(prompt)
        return reply