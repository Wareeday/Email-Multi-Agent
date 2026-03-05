from app.agents.manager_agent import ManagerAgent
from app.agents.support_agent import SupportAgent
from app.agents.sales_agent import SalesAgent
from app.agents.escalation_agent import EscalationAgent
from app.services.memory_service import get_or_create_customer, get_conversation_history, save_conversation
from app.services.sentiment_service import analyze_sentiment, update_customer_sentiment
from app.email.smtp_client import send_email
from app.utils.logger import logger
import asyncio

manager = ManagerAgent()
support = SupportAgent()
sales = SalesAgent()
escalation = EscalationAgent()

async def process_email(email_data: dict):
    """Main orchestrator: handles an incoming email."""
    try:
        from_email = email_data["from"]
        subject = email_data["subject"]
        body = email_data["body"]

        # 1. Get or create customer
        customer = await get_or_create_customer(from_email)

        # 2. Load conversation history
        history = await get_conversation_history(customer.id)

        # 3. Analyze sentiment of new email
        sentiment = analyze_sentiment(body)
        # Update running sentiment for customer
        await update_customer_sentiment(customer.id, sentiment)

        # 4. Retrieve knowledge base context (RAG) – handled inside agents
        # 5. Manager classifies intent
        intent = await manager.classify(subject, body, sentiment)

        # 6. Select agent and generate reply
        if intent == "sales":
            reply = await sales.generate_reply(from_email, history, body)
        elif intent == "escalation" or customer.sentiment_score < -5:
            # Escalate if sentiment too low
            reply = await escalation.generate_reply(from_email, history, body)
            intent = "escalation"  # override
        else:
            reply = await support.generate_reply(from_email, history, body)

        # 7. Save conversation to DB
        await save_conversation(customer.id, subject, body, reply)

        # 8. Send reply via email
        send_email(from_email, f"Re: {subject}", reply)

        logger.info(f"Processed email from {from_email} with intent {intent}")
    except Exception as e:
        logger.error(f"Error processing email: {e}")