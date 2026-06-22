from services.telegram_service import send_telegram_message, TelegramNotificationError
from services.email_service import send_backup_email, EmailNotificationError


def build_housekeeping_message(room, booking=None) -> str:
    """
    Builds a data-minimised housekeeping message.

    The message avoids guest names, phone numbers, payment details and identity
    information because housekeeping only needs operational room information.
    """
    room_number = getattr(room, "number", None) or getattr(room, "room_number", "Unknown")
    status = getattr(room, "status", "Cleaning Required")

    return (
        "Housekeeping alert\n"
        f"Room: {room_number}\n"
        "Task: Cleaning required\n"
        f"Status: {status}\n"
        "Priority: Normal"
    )


def send_housekeeping_notification(room, booking=None) -> dict:
    """
    Sends a housekeeping notification using a primary API and backup API.

    Primary channel: Telegram.
    Backup channel: Email.
    """
    message = build_housekeeping_message(room, booking)

    try:
        telegram_result = send_telegram_message(message)

        return {
            "success": True,
            "channel": "telegram",
            "message": message,
            "error": None,
            "details": telegram_result,
        }

    except TelegramNotificationError as telegram_error:
        try:
            email_result = send_backup_email(
                subject="Housekeeping alert: room requires cleaning",
                message=message,
            )

            return {
                "success": True,
                "channel": "email",
                "message": message,
                "error": f"Primary API failed: {telegram_error}",
                "details": email_result,
            }

        except EmailNotificationError as email_error:
            return {
                "success": False,
                "channel": "failed",
                "message": message,
                "error": (
                    f"Primary API failed: {telegram_error}; "
                    f"Backup API failed: {email_error}"
                ),
                "details": None,
            }