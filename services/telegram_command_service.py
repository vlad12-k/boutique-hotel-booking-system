

"""Telegram staff command handling for hotel operations."""

from __future__ import annotations

from models import NotificationLog, Room, db


HELP_MESSAGE = """Hotel staff bot commands:
/help - show available commands
/status - show room status summary
/cleaning - list rooms waiting for housekeeping
/available - list available rooms
/ready <room number> - mark a cleaned room as Available
/maintenance <room number> - mark a room as Maintenance
/notifications - show the latest notification logs"""


def handle_telegram_command(text: str) -> str:
    """Routes a Telegram command to the correct hotel operation."""
    command_text = (text or "").strip()

    if not command_text:
        return HELP_MESSAGE

    parts = command_text.split()
    command = parts[0].lower()

    if command in {"/help", "help"}:
        return HELP_MESSAGE

    if command == "/status":
        return build_room_status_summary()

    if command == "/cleaning":
        return build_room_list_by_status("Cleaning", "Rooms waiting for housekeeping")

    if command == "/available":
        return build_room_list_by_status("Available", "Available rooms")

    if command == "/ready":
        return mark_room_status_from_command(parts, "Available", "Room cleaned and ready")

    if command == "/maintenance":
        return mark_room_status_from_command(parts, "Maintenance", "Room marked for maintenance")

    if command == "/notifications":
        return build_recent_notification_summary()

    return f"Unknown command: {command}\n\n{HELP_MESSAGE}"


def build_room_status_summary() -> str:
    """Builds a count summary for all room statuses."""
    rooms = Room.query.order_by(Room.room_number.asc()).all()

    if not rooms:
        return "No rooms are currently registered in the system."

    counts: dict[str, int] = {}
    for room in rooms:
        counts[room.status] = counts.get(room.status, 0) + 1

    lines = ["Room status summary"]
    for status in sorted(counts):
        lines.append(f"{status}: {counts[status]}")

    return "\n".join(lines)


def build_room_list_by_status(status: str, title: str) -> str:
    """Lists rooms matching a specific status."""
    rooms = Room.query.filter_by(status=status).order_by(Room.room_number.asc()).all()

    if not rooms:
        return f"{title}\nNo rooms found."

    lines = [title]
    for room in rooms:
        lines.append(f"Room {room.room_number} - {room.room_type} - {room.status}")

    return "\n".join(lines)


def mark_room_status_from_command(parts: list[str], new_status: str, action_label: str) -> str:
    """Updates a room status from a Telegram command and logs the action."""
    if len(parts) != 2:
        return f"Usage: {parts[0]} <room number>"

    room_number = parts[1]
    room = Room.query.filter_by(room_number=room_number).first()

    if room is None:
        return f"Room {room_number} was not found."

    previous_status = room.status
    room.status = new_status

    message = (
        f"{action_label}\n"
        f"Room: {room.room_number}\n"
        f"Previous status: {previous_status}\n"
        f"New status: {new_status}"
    )

    notification_log = NotificationLog(
        room_id=room.id,
        booking_id=None,
        channel="telegram-command",
        status="Sent",
        message=message,
        error_message=None,
    )

    db.session.add(notification_log)
    db.session.commit()

    return message


def build_recent_notification_summary(limit: int = 5) -> str:
    """Shows the most recent notification log entries."""
    logs = NotificationLog.query.order_by(NotificationLog.created_at.desc()).limit(limit).all()

    if not logs:
        return "No notification logs found."

    lines = [f"Latest {len(logs)} notification log entries"]
    for log in logs:
        room_number = log.room.room_number if log.room else "N/A"
        lines.append(
            f"#{log.id} | Room {room_number} | {log.channel} | {log.status}"
        )

    return "\n".join(lines)