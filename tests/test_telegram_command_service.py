

from services.telegram_command_service import HELP_MESSAGE, handle_telegram_command


def test_help_command_returns_staff_command_list():
    response = handle_telegram_command("/help")

    assert "Hotel staff bot commands" in response
    assert "/status" in response
    assert "/cleaning" in response
    assert "/ready <room number>" in response
    assert "/maintenance <room number>" in response
    assert "/notifications" in response


def test_empty_command_returns_help_message():
    response = handle_telegram_command("")

    assert response == HELP_MESSAGE


def test_unknown_command_returns_help_guidance():
    response = handle_telegram_command("/unknown")

    assert "Unknown command: /unknown" in response
    assert "Hotel staff bot commands" in response


def test_ready_command_requires_room_number():
    response = handle_telegram_command("/ready")

    assert response == "Usage: /ready <room number>"


def test_maintenance_command_requires_room_number():
    response = handle_telegram_command("/maintenance")

    assert response == "Usage: /maintenance <room number>"