from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

ROOM_STATUSES = ["Available", "Occupied", "Cleaning", "Maintenance"]
BOOKING_STATUSES = ["Pending", "Confirmed", "Checked-in", "Checked-out", "Cancelled"]
ACTIVE_BOOKING_STATUSES = ["Pending", "Confirmed", "Checked-in"]


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.Text)

    bookings = db.relationship(
        "Booking",
        back_populates="guest",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Guest {self.id}: {self.full_name}>"


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Available")

    bookings = db.relationship(
        "Booking",
        back_populates="room",
        cascade="all, delete-orphan",
    )
    notification_logs = db.relationship(
        "NotificationLog",
        back_populates="room",
    )

    def __repr__(self):
        return f"<Room {self.id}: {self.room_number}>"


class NotificationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=True)
    channel = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    room = db.relationship("Room", back_populates="notification_logs")
    booking = db.relationship("Booking", back_populates="notification_logs")

    def __repr__(self):
        return f"<NotificationLog {self.id}: {self.channel}/{self.status}>"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    guest = db.relationship("Guest", back_populates="bookings")
    room = db.relationship("Room", back_populates="bookings")
    notification_logs = db.relationship(
        "NotificationLog",
        back_populates="booking",
    )

    def __repr__(self):
        return (
            f"<Booking {self.id}: guest={self.guest_id}, "
            f"room={self.room_id}, status={self.status}>"
        )