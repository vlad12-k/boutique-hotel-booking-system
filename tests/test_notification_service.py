from services.notification_service import build_housekeeping_message, build_room_ready_message


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