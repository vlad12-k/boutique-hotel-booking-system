import os
import smtplib
from email.message import EmailMessage


class EmailNotificationError(Exception):
    """Raised when backup email delivery fails."""


def get_email_port() -> int:
    """Returns the configured SMTP port."""
    try:
        return int(os.getenv("EMAIL_PORT", "587"))
    except ValueError as exc:
        raise EmailNotificationError("Email port must be a valid number.") from exc


def get_email_config() -> dict:
    """Reads SMTP email configuration from environment variables."""
    email_host = os.getenv("EMAIL_HOST")
    email_port = get_email_port()
    email_username = os.getenv("EMAIL_USERNAME") or os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_from = os.getenv("EMAIL_FROM") or email_username
    email_to = os.getenv("EMAIL_TO") or os.getenv("HOUSEKEEPING_EMAIL")

    if not all([email_host, email_username, email_password, email_from, email_to]):
        raise EmailNotificationError("Email credentials are not configured.")

    return {
        "host": email_host,
        "port": email_port,
        "username": email_username,
        "password": email_password,
        "from": email_from,
        "to": email_to,
    }


def send_backup_email(subject: str, message: str) -> dict:
    """
    Sends a backup housekeeping notification by email.

    This fallback is used when the primary messaging API fails.
    """
    config = get_email_config()

    email = EmailMessage()
    email["From"] = config["from"]
    email["To"] = config["to"]
    email["Subject"] = subject
    email.set_content(message)

    try:
        with smtplib.SMTP(config["host"], config["port"], timeout=10) as server:
            server.starttls()
            server.login(config["username"], config["password"])
            server.send_message(email)

        return {
            "success": True,
            "channel": "email",
            "to": config["to"],
            "host": config["host"],
        }

    except Exception as exc:
        raise EmailNotificationError(
            "Email fallback delivery failed without exposing credentials."
        ) from exc