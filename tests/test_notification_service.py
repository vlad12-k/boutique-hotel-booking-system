import pytest
import services.notification_service as notification_service
import services.telegram_service as telegram_service
from services.notification_service import (
    build_housekeeping_message,
    build_room_ready_message,
    send_housekeeping_notification,
    send_room_ready_notification,
)


class DummyRoom:
    room_number = "101"
    status = "Cleaning Required"


def test_housekeeping_message_excludes_guest_personal_data():
    room = DummyRoom()

    message = build_housekeeping_message(room)

    assert "101" in message
    assert "Cleaning required" in message
    assert "guest" not in message.lower()
    assert "phone" not in message.lower()
    assert "passport" not in message.lower()
    assert "payment" not in message.lower()


def test_housekeeping_message_uses_room_number_attribute():
    class RoomWithRoomNumber:
        room_number = "110"
        status = "Cleaning"

    message = build_housekeeping_message(RoomWithRoomNumber())

    assert "110" in message
    assert "Cleaning required" in message
    assert "John" not in message
    assert "Smith" not in message


def test_room_ready_message_excludes_guest_personal_data():
    class ReadyRoom:
        room_number = "103"
        status = "Available"

    message = build_room_ready_message(ReadyRoom())

    assert "Housekeeping complete" in message
    assert "Room: 103" in message
    assert "Room cleaned and ready" in message
    assert "Status: Available" in message
    assert "guest" not in message.lower()
    assert "phone" not in message.lower()
    assert "passport" not in message.lower()
    assert "payment" not in message.lower()


def test_housekeeping_notification_uses_email_backup_when_telegram_fails(monkeypatch):
    class RoomWithRoomNumber:
        room_number = "110"
        status = "Cleaning"

    def fake_telegram_message(message):
        raise notification_service.TelegramNotificationError("Telegram unavailable")

    def fake_backup_email(subject, message):
        return {
            "success": True,
            "channel": "email",
            "to": "housekeeping@example.com",
            "host": "sandbox.smtp.mailtrap.io",
        }

    monkeypatch.setattr(
        notification_service,
        "send_telegram_message",
        fake_telegram_message,
    )
    monkeypatch.setattr(notification_service, "send_backup_email", fake_backup_email)

    result = send_housekeeping_notification(RoomWithRoomNumber())

    assert result["success"] is True
    assert result["channel"] == "email"
    assert "Cleaning required" in result["message"]
    assert "Primary API failed" in result["error"]
    assert result["details"]["host"] == "sandbox.smtp.mailtrap.io"


# New test: uses telegram when primary delivery succeeds
def test_housekeeping_notification_uses_telegram_when_primary_delivery_succeeds(monkeypatch):
    class RoomWithRoomNumber:
        room_number = "110"
        status = "Cleaning"

    email_called = False

    def fake_telegram_message(message):
        return {
            "success": True,
            "channel": "telegram",
            "response": {"ok": True},
        }

    def fake_backup_email(subject, message):
        nonlocal email_called
        email_called = True
        return {
            "success": True,
            "channel": "email",
        }

    monkeypatch.setattr(
        notification_service,
        "send_telegram_message",
        fake_telegram_message,
    )
    monkeypatch.setattr(notification_service, "send_backup_email", fake_backup_email)

    result = send_housekeeping_notification(RoomWithRoomNumber())

    assert result["success"] is True
    assert result["channel"] == "telegram"
    assert "Cleaning required" in result["message"]
    assert email_called is False


# New test: returns failed when both channels fail
def test_housekeeping_notification_returns_failed_when_both_channels_fail(monkeypatch):
    class RoomWithRoomNumber:
        room_number = "110"
        status = "Cleaning"

    def fake_telegram_message(message):
        raise notification_service.TelegramNotificationError("Telegram unavailable")

    def fake_backup_email(subject, message):
        raise notification_service.EmailNotificationError("Email fallback unavailable")

    monkeypatch.setattr(
        notification_service,
        "send_telegram_message",
        fake_telegram_message,
    )
    monkeypatch.setattr(notification_service, "send_backup_email", fake_backup_email)

    result = send_housekeeping_notification(RoomWithRoomNumber())

    assert result["success"] is False
    assert result["channel"] == "failed"
    assert "Cleaning required" in result["message"]
    assert "Primary API and backup email delivery failed" in result["error"]


def test_room_ready_notification_uses_email_backup_when_telegram_fails(monkeypatch):
    class ReadyRoom:
        room_number = "103"
        status = "Available"

    def fake_telegram_message(message):
        raise notification_service.TelegramNotificationError("Telegram unavailable")

    def fake_backup_email(subject, message):
        return {
            "success": True,
            "channel": "email",
            "to": "housekeeping@example.com",
            "host": "sandbox.smtp.mailtrap.io",
        }

    monkeypatch.setattr(
        notification_service,
        "send_telegram_message",
        fake_telegram_message,
    )
    monkeypatch.setattr(notification_service, "send_backup_email", fake_backup_email)

    result = send_room_ready_notification(ReadyRoom())

    assert result["success"] is True
    assert result["channel"] == "email"
    assert "Housekeeping complete" in result["message"]
    assert "Primary API failed" in result["error"]
    assert result["details"]["host"] == "sandbox.smtp.mailtrap.io"


def test_telegram_error_message_does_not_expose_token(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:SECRET_TOKEN")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    def fake_post(*args, **kwargs):
        raise telegram_service.requests.RequestException(
            "Failed request to https://api.telegram.org/bot123456:SECRET_TOKEN/sendMessage"
        )

    monkeypatch.setattr(telegram_service.requests, "post", fake_post)

    with pytest.raises(telegram_service.TelegramNotificationError) as exc_info:
        telegram_service.send_telegram_message("Test message")

    error_text = str(exc_info.value)
    assert "SECRET_TOKEN" not in error_text
    assert "bot123456" not in error_text
    assert "api.telegram.org/bot" not in error_text


def test_telegram_send_message_handles_ok_false(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:TEST")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": False, "description": "Bad Request"}

    monkeypatch.setattr(
        telegram_service.requests,
        "post",
        lambda *args, **kwargs: FakeResponse(),
    )

    with pytest.raises(telegram_service.TelegramNotificationError) as exc_info:
        telegram_service.send_telegram_message("Test message")

    assert "unsuccessful" in str(exc_info.value)