from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    database_url: str = os.getenv("DATABASE_URL")
    imap_server: str = os.getenv("IMAP_SERVER")
    imap_port: int = int(os.getenv("IMAP_PORT", 993))
    imap_username: str = os.getenv("IMAP_USERNAME")
    imap_password: str = os.getenv("IMAP_PASSWORD")
    smtp_server: str = os.getenv("SMTP_SERVER")
    smtp_port: int = int(os.getenv("SMTP_PORT", 587))
    smtp_username: str = os.getenv("SMTP_USERNAME")
    smtp_password: str = os.getenv("SMTP_PASSWORD")
    sentiment_threshold: int = int(os.getenv("SENTIMENT_THRESHOLD", -5))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()