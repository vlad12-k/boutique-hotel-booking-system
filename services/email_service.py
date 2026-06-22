import os
import smtplib
from email.message import EmailMessage


class EmailNotificationError(Exception):
    """Raised when backup email delivery fails."""


def send_backup_email(subject: str, message: str) -> dict:
    """
    Sends a backup housekeeping notification by email.

    This fallback is used when the primary messaging API fails.
    """
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT", "587"))
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    housekeeping_email = os.getenv("HOUSEKEEPING_EMAIL")

    if not all([email_host, email_user, email_password, housekeeping_email]):
        raise EmailNotificationError("Email credentials are not configured.")

    email = EmailMessage()
    email["From"] = email_user
    email["To"] = housekeeping_email
    email["Subject"] = subject
    email.set_content(message)

    try:
        with smtplib.SMTP(email_host, email_port, timeout=10) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(email)

        return {
            "success": True,
            "channel": "email",
        }

    except Exception as exc:
        raise EmailNotificationError(str(exc)) from exc