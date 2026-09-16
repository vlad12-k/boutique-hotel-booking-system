from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from hotel_app.extensions import db


ROOM_STATUSES = ["Available", "Occupied", "Cleaning", "Maintenance"]
BOOKING_STATUSES = ["Pending", "Confirmed", "Checked-in", "Checked-out", "Cancelled"]
ACTIVE_BOOKING_STATUSES = ["Pending", "Confirmed", "Checked-in"]
STAFF_ROLES = ["owner", "staff"]


class StaffAccount(UserMixin, db.Model):
    __tablename__ = "staff_account"
    __table_args__ = (
        db.CheckConstraint(
            "role IN ('owner', 'staff')",
            name="ck_staff_account_role",
        ),
        db.CheckConstraint(
            "email = lower(email)",
            name="ck_staff_account_email_normalised",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="staff")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    password_changed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)

    audit_events = db.relationship(
        "SecurityAuditEvent",
        back_populates="staff_account",
        passive_deletes=True,
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="scrypt")
        self.password_changed_at = datetime.now(timezone.utc)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<StaffAccount id={self.id} role={self.role}>"


class SecurityAuditEvent(db.Model):
    __tablename__ = "security_audit_event"
    __table_args__ = (
        db.Index(
            "ix_security_audit_event_type_created",
            "event_type",
            "created_at",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    staff_account_id = db.Column(
        db.Integer,
        db.ForeignKey("staff_account.id", ondelete="SET NULL"),
        nullable=True,
    )
    event_type = db.Column(db.String(50), nullable=False)
    outcome = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    staff_account = db.relationship(
        "StaffAccount",
        back_populates="audit_events",
    )

    def __repr__(self):
        return f"<SecurityAuditEvent id={self.id} type={self.event_type}>"


class Guest(db.Model):
    __tablename__ = "guest"

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
        return f"<Guest id={self.id}>"


class Room(db.Model):
    __tablename__ = "room"

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
    __tablename__ = "notification_log"

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
    __tablename__ = "booking"
    __table_args__ = (
        db.CheckConstraint(
            "check_out_date > check_in_date",
            name="ck_booking_valid_stay_period",
        ),
        db.CheckConstraint(
            "total_price >= 0",
            name="ck_booking_non_negative_total",
        ),
        db.Index(
            "ix_booking_room_dates",
            "room_id",
            "check_in_date",
            "check_out_date",
        ),
    )

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
