import os
import requests


class TelegramNotificationError(Exception):
    """Raised when Telegram notification delivery fails."""


def send_telegram_message(message: str) -> dict:
    """
    Sends a housekeeping notification through Telegram Bot API.

    API credentials are loaded from environment variables to avoid hardcoding
    secrets in the source code.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise TelegramNotificationError("Telegram credentials are not configured.")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        return {
            "success": True,
            "channel": "telegram",
            "response": response.json(),
        }

    except requests.RequestException as exc:
        raise TelegramNotificationError(str(exc)) from exc