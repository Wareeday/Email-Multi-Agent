from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.orchestrator import process_email
from app.database.crud import get_customer_by_email
from app.email.imap_client import fetch_unseen_emails
from app.utils.logger import logger
import asyncio

router = APIRouter()

@router.post("/process-emails")
async def process_emails_endpoint(background_tasks: BackgroundTasks):
    """Fetch unseen emails and trigger processing in background."""
    try:
        emails = fetch_unseen_emails()
        for email_data in emails:
            background_tasks.add_task(process_email, email_data)
        return {"status": "processing", "count": len(emails)}
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}

# Optional: endpoint to manually process a single email (for testing)
@router.post("/process-single")
async def process_single(email_data: dict):
    await process_email(email_data)
    return {"status": "processed"}