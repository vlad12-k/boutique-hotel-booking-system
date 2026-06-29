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
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    return send_telegram_reply(chat_id, message)


def get_telegram_bot_token() -> str:
    """Returns the configured Telegram bot token."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        raise TelegramNotificationError("Telegram bot token is not configured.")

    return bot_token


def send_telegram_reply(chat_id: str | int | None, message: str) -> dict:
    """
    Sends a Telegram message to a specific chat.

    This is used by both outbound system notifications and the interactive
    Telegram staff command worker.
    """
    bot_token = get_telegram_bot_token()

    if not chat_id:
        raise TelegramNotificationError("Telegram chat ID is not configured.")

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


def get_telegram_updates(offset: int | None = None, timeout: int = 10) -> list[dict]:
    """Fetches Telegram updates using long polling."""
    bot_token = get_telegram_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    payload = {
        "timeout": timeout,
    }

    if offset is not None:
        payload["offset"] = offset

    try:
        response = requests.get(url, params=payload, timeout=timeout + 5)
        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            raise TelegramNotificationError("Telegram getUpdates returned an unsuccessful response.")

        return data.get("result", [])

    except requests.RequestException as exc:
        raise TelegramNotificationError(str(exc)) from exc


def get_allowed_chat_ids() -> set[str]:
    """Reads authorised staff chat IDs from the environment."""
    configured_chat_ids = os.getenv("TELEGRAM_ALLOWED_CHAT_IDS") or os.getenv("TELEGRAM_CHAT_ID", "")

    return {
        chat_id.strip()
        for chat_id in configured_chat_ids.split(",")
        if chat_id.strip()
    }


def is_authorised_chat(chat_id: str | int | None) -> bool:
    """Checks whether an incoming Telegram chat is authorised."""
    if chat_id is None:
        return False

    allowed_chat_ids = get_allowed_chat_ids()

    if not allowed_chat_ids:
        return False

    return str(chat_id) in allowed_chat_ids