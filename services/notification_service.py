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


def build_room_ready_message(room) -> str:
    """
    Builds a data-minimised room-ready message.

    This message is sent after housekeeping has completed cleaning and staff
    mark the room as available again. It avoids guest names, phone numbers,
    payment details and identity information because the notification only
    needs operational room information.
    """
    room_number = getattr(room, "number", None) or getattr(room, "room_number", "Unknown")
    status = getattr(room, "status", "Available")

    return (
        "Housekeeping complete\n"
        f"Room: {room_number}\n"
        "Task: Room cleaned and ready\n"
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


def send_room_ready_notification(room) -> dict:
    """
    Sends a notification when a cleaned room is made available again.

    Primary channel: Telegram.
    Backup channel: Email.
    """
    message = build_room_ready_message(room)
    room_number = getattr(room, "number", None) or getattr(room, "room_number", "Unknown")

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
                subject=f"Housekeeping complete: room {room_number} is available",
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