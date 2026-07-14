"""Telegram long-polling worker for hotel staff commands.

Run this file in a separate terminal while the Flask application is available:

    python telegram_bot_worker.py

The worker receives Telegram messages, checks whether the chat is authorised,
routes supported commands to the hotel command service, and replies in Telegram.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from dotenv import load_dotenv

from app import app
from services.telegram_command_service import handle_telegram_command
from services.telegram_service import (
    TelegramNotificationError,
    get_telegram_updates,
    is_authorised_chat,
    send_telegram_reply,
)


ACCESS_DENIED_MESSAGE = "Access denied. This bot is restricted to authorised hotel staff."
DEFAULT_POLL_INTERVAL_SECONDS = 3


def get_poll_interval_seconds() -> int:
    """Returns the configured polling delay between Telegram update checks."""
    configured_interval = os.getenv("TELEGRAM_POLL_INTERVAL_SECONDS", str(DEFAULT_POLL_INTERVAL_SECONDS))

    try:
        interval = int(configured_interval)
    except ValueError:
        return DEFAULT_POLL_INTERVAL_SECONDS

    return max(1, interval)


def extract_message(update: dict) -> tuple[int | None, str | None, str | None]:
    """Extracts chat id, text and sender name from a Telegram update."""
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    from_user = message.get("from") or {}

    chat_id = chat.get("id")
    text = message.get("text")
    sender_name = from_user.get("first_name") or from_user.get("username") or "Unknown"

    return chat_id, text, sender_name


def process_update(update: dict) -> None:
    """Processes one Telegram update and sends an appropriate reply."""
    chat_id, text, sender_name = extract_message(update)

    if chat_id is None or not text:
        return

    if not is_authorised_chat(chat_id):
        send_telegram_reply(chat_id, ACCESS_DENIED_MESSAGE)
        print("Rejected unauthorised Telegram chat.")
        return

    with app.app_context():
        reply = handle_telegram_command(text)

    send_telegram_reply(chat_id, reply)
    print("Processed authorised Telegram staff command.")


def run_worker() -> None:
    """Runs the Telegram long-polling loop."""
    load_dotenv(Path(".env"))

    print("Telegram staff bot worker started.")
    print("Press CTRL+C to stop.")

    offset = None
    poll_interval = get_poll_interval_seconds()

    while True:
        try:
            updates = get_telegram_updates(offset=offset, timeout=10)

            for update in updates:
                update_id = update.get("update_id")
                if update_id is not None:
                    offset = update_id + 1

                process_update(update)

        except TelegramNotificationError as exc:
            print(f"Telegram worker API error: {exc}")
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("Telegram staff bot worker stopped.")
            break

        except Exception:  # noqa: BLE001 - worker should not crash during demo use
            print("Unexpected Telegram worker error occurred.")
            time.sleep(poll_interval)


if __name__ == "__main__":
    run_worker()
