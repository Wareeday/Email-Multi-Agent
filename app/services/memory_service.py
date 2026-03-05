from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import AsyncSessionLocal
from app.database import crud
from app.database.models import Customer, Conversation

async def get_or_create_customer(email: str) -> Customer:
    async with AsyncSessionLocal() as session:
        customer = await crud.get_customer_by_email(session, email)
        if not customer:
            customer = await crud.create_customer(session, email)
        return customer

async def get_conversation_history(customer_id: int) -> str:
    async with AsyncSessionLocal() as session:
        convs = await crud.get_conversations_by_customer(session, customer_id, limit=10)
        history = "\n".join([f"User: {c.message}\nAI: {c.reply}" for c in convs])
        return history

async def save_conversation(customer_id: int, subject: str, message: str, reply: str):
    async with AsyncSessionLocal() as session:
        await crud.create_conversation(session, customer_id, subject, message, reply)

async def update_customer_sentiment(customer_id: int, sentiment_delta: float):
    async with AsyncSessionLocal() as session:
        await crud.update_customer_sentiment(session, customer_id, sentiment_delta)