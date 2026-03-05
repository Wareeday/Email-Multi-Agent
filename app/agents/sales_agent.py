from app.ai.llm import get_llm
from app.ai.prompts import SALES_REPLY_PROMPT
from app.services.rag_service import retrieve_relevant_knowledge

class SalesAgent:
    def __init__(self):
        self.llm = get_llm()

    async def generate_reply(self, customer_email: str, conversation_history: str, email_body: str) -> str:
        knowledge = retrieve_relevant_knowledge(email_body, top_k=3)
        prompt = SALES_REPLY_PROMPT.format(
            history=conversation_history,
            knowledge=knowledge,
            email_body=email_body
        )
        reply = await self.llm.acomplete(prompt)
        return reply