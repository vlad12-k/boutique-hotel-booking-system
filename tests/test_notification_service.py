import services.notification_service as notification_service
from services.notification_service import (
    build_housekeeping_message,
    build_room_ready_message,
    send_housekeeping_notification,
    send_room_ready_notification,
)


class DummyRoom:
    number = "101"
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
        number = "103"
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