import imaplib
import email
from email.utils import parsedate_to_datetime
from app.config.settings import settings
from app.utils.logger import logger

def fetch_unseen_emails():
    """Fetch unseen emails from inbox. Returns list of dicts with subject, from, body, date."""
    try:
        mail = imaplib.IMAP4_SSL(settings.imap_server, settings.imap_port)
        mail.login(settings.imap_username, settings.imap_password)
        mail.select("inbox")

        result, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()
        emails = []

        for e_id in email_ids:
            result, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract subject
            subject = msg.get("Subject", "")

            # Extract from
            from_ = msg.get("From", "")

            # Extract date
            date_str = msg.get("Date", "")
            date = parsedate_to_datetime(date_str) if date_str else None

            # Extract body (plain text)
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            emails.append({
                "id": e_id.decode(),
                "from": from_,
                "subject": subject,
                "body": body,
                "date": date
            })

        mail.close()
        mail.logout()
        return emails
    except Exception as e:
        logger.error(f"IMAP fetch error: {e}")
        return []