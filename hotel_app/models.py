from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import event as sqlalchemy_event
from werkzeug.security import check_password_hash, generate_password_hash

from hotel_app.domain import BookingSource, PaymentStatus, RoomOperationalState
from hotel_app.extensions import db


ROOM_OPERATIONAL_STATES = [state.value for state in RoomOperationalState]
ROOM_STATUSES = ["Available", "Cleaning", "Maintenance"]
BOOKING_STATUSES = [
    "Pending",
    "Confirmed",
    "Rejected",
    "Checked-in",
    "Checked-out",
    "Cancelled",
]
ACTIVE_BOOKING_STATUSES = ["Pending", "Confirmed", "Checked-in"]
BOOKING_SOURCES = [source.value for source in BookingSource]
PAYMENT_STATUSES = [status.value for status in PaymentStatus]
BOOKING_EVENT_TYPES = [
    "created",
    "modified",
    "confirmed",
    "rejected",
    "cancelled",
    "room_reassigned",
    "checked_in",
    "checked_out",
    "legacy_migrated",
]
STAFF_ROLES = ["owner", "staff"]


class StaffAccount(UserMixin, db.Model):
    __tablename__ = "staff_account"
    __table_args__ = (
        db.CheckConstraint("role IN ('owner', 'staff')", name="ck_staff_account_role"),
        db.CheckConstraint(
            "email = lower(email)", name="ck_staff_account_email_normalised"
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
        "SecurityAuditEvent", back_populates="staff_account", passive_deletes=True
    )
    booking_events = db.relationship(
        "BookingEvent", back_populates="actor", passive_deletes=True
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
        db.Index("ix_security_audit_event_type_created", "event_type", "created_at"),
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

    staff_account = db.relationship("StaffAccount", back_populates="audit_events")

    def __repr__(self):
        return f"<SecurityAuditEvent id={self.id} type={self.event_type}>"


class Guest(db.Model):
    __tablename__ = "guest"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    notes = db.Column(db.Text)

    bookings = db.relationship("Booking", back_populates="guest")

    def __repr__(self):
        return f"<Guest id={self.id}>"


class RoomType(db.Model):
    __tablename__ = "room_type"
    __table_args__ = (
        db.CheckConstraint(
            "bathroom_type IN ('private', 'shared', 'unspecified')",
            name="ck_room_type_bathroom_type",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    bathroom_type = db.Column(db.String(20), nullable=False)
    has_balcony_or_terrace = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    rooms = db.relationship("Room", back_populates="room_type")

    def __repr__(self):
        return f"<RoomType {self.code}>"


class Room(db.Model):
    __tablename__ = "room"
    __table_args__ = (
        db.CheckConstraint("price_per_night >= 0", name="ck_room_non_negative_price"),
        db.CheckConstraint(
            "length(currency) = 3 AND currency = upper(currency)",
            name="ck_room_currency",
        ),
        db.CheckConstraint(
            "operational_state IN ('ready', 'cleaning', 'maintenance')",
            name="ck_room_operational_state",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    room_type_id = db.Column(
        db.Integer, db.ForeignKey("room_type.id"), nullable=False
    )
    price_per_night = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="ILS")
    operational_state = db.Column(
        db.String(20), nullable=False, default=RoomOperationalState.READY.value
    )

    room_type = db.relationship("RoomType", back_populates="rooms")
    bookings = db.relationship("Booking", back_populates="room")
    notification_logs = db.relationship("NotificationLog", back_populates="room")

    def is_occupied(self) -> bool:
        """Return physical occupancy derived from checked-in bookings."""
        if self.id is None:
            return any(booking.status == "Checked-in" for booking in self.bookings)
        return (
            db.session.query(Booking.id)
            .filter(Booking.room_id == self.id, Booking.status == "Checked-in")
            .first()
            is not None
        )

    @property
    def status(self) -> str:
        """Compatibility display status; occupancy is never persisted here."""
        if self.is_occupied():
            return "Occupied"
        return {
            RoomOperationalState.READY.value: "Available",
            RoomOperationalState.CLEANING.value: "Cleaning",
            RoomOperationalState.MAINTENANCE.value: "Maintenance",
        }[self.operational_state]

    @property
    def operational_status(self) -> str:
        return {
            RoomOperationalState.READY.value: "Available",
            RoomOperationalState.CLEANING.value: "Cleaning",
            RoomOperationalState.MAINTENANCE.value: "Maintenance",
        }[self.operational_state]

    @status.setter
    def status(self, value: str) -> None:
        if value == "Occupied":
            raise ValueError("Room occupancy is derived from checked-in bookings.")
        state_by_legacy_label = {
            "Available": RoomOperationalState.READY.value,
            "Cleaning": RoomOperationalState.CLEANING.value,
            "Maintenance": RoomOperationalState.MAINTENANCE.value,
        }
        self.operational_state = state_by_legacy_label.get(value, value)

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
            "check_out_date > check_in_date", name="ck_booking_valid_stay_period"
        ),
        db.CheckConstraint("total_price >= 0", name="ck_booking_non_negative_total"),
        db.CheckConstraint(
            "length(currency) = 3 AND currency = upper(currency)",
            name="ck_booking_currency",
        ),
        db.CheckConstraint(
            "source IN ('direct', 'phone', 'walk_in', 'booking_com', 'other')",
            name="ck_booking_source",
        ),
        db.CheckConstraint(
            "status IN ('Pending', 'Confirmed', 'Rejected', 'Checked-in', "
            "'Checked-out', 'Cancelled')",
            name="ck_booking_status",
        ),
        db.CheckConstraint(
            "(external_provider IS NULL AND external_reference IS NULL) OR "
            "(external_provider IS NOT NULL AND external_reference IS NOT NULL)",
            name="ck_booking_external_reference_pair",
        ),
        db.UniqueConstraint(
            "external_provider",
            "external_reference",
            name="uq_booking_external_reference",
        ),
        db.Index(
            "ix_booking_room_dates", "room_id", "check_in_date", "check_out_date"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    source = db.Column(db.String(20), nullable=False, default=BookingSource.DIRECT.value)
    external_provider = db.Column(db.String(50), nullable=True)
    external_reference = db.Column(db.String(120), nullable=True)
    total_price = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="ILS")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    guest = db.relationship("Guest", back_populates="bookings")
    room = db.relationship("Room", back_populates="bookings")
    notification_logs = db.relationship("NotificationLog", back_populates="booking")
    events = db.relationship(
        "BookingEvent",
        back_populates="booking",
        order_by="BookingEvent.occurred_at, BookingEvent.id",
    )
    payments = db.relationship("Payment", back_populates="booking")

    def __repr__(self):
        return (
            f"<Booking {self.id}: guest={self.guest_id}, "
            f"room={self.room_id}, status={self.status}>"
        )


class BookingEvent(db.Model):
    __tablename__ = "booking_event"
    __table_args__ = (
        db.CheckConstraint(
            "event_type IN ('created', 'modified', 'confirmed', 'rejected', "
            "'cancelled', 'room_reassigned', 'checked_in', 'checked_out', "
            "'legacy_migrated')",
            name="ck_booking_event_type",
        ),
        db.Index("ix_booking_event_booking_occurred", "booking_id", "occurred_at"),
    )

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    event_type = db.Column(db.String(30), nullable=False)
    from_status = db.Column(db.String(20), nullable=True)
    to_status = db.Column(db.String(20), nullable=True)
    from_room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=True)
    to_room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=True)
    actor_staff_account_id = db.Column(
        db.Integer,
        db.ForeignKey("staff_account.id"),
        nullable=True,
    )
    occurred_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    booking = db.relationship("Booking", back_populates="events")
    actor = db.relationship("StaffAccount", back_populates="booking_events")
    from_room = db.relationship("Room", foreign_keys=[from_room_id])
    to_room = db.relationship("Room", foreign_keys=[to_room_id])

    def __repr__(self):
        return f"<BookingEvent {self.id}: {self.event_type}>"


@sqlalchemy_event.listens_for(BookingEvent, "before_update")
def _prevent_booking_event_update(*_args) -> None:
    raise ValueError("Booking events are append-only and cannot be updated.")


@sqlalchemy_event.listens_for(BookingEvent, "before_delete")
def _prevent_booking_event_delete(*_args) -> None:
    raise ValueError("Booking events are append-only and cannot be deleted.")


class Payment(db.Model):
    __tablename__ = "payment"
    __table_args__ = (
        db.CheckConstraint("amount >= 0", name="ck_payment_non_negative_amount"),
        db.CheckConstraint(
            "length(currency) = 3 AND currency = upper(currency)",
            name="ck_payment_currency",
        ),
        db.CheckConstraint(
            "status IN ('unpaid', 'deposit_due', 'deposit_paid', "
            "'paid_in_full', 'refunded')",
            name="ck_payment_status",
        ),
        db.CheckConstraint(
            "(external_provider IS NULL AND external_reference IS NULL) OR "
            "(external_provider IS NOT NULL AND external_reference IS NOT NULL)",
            name="ck_payment_external_reference_pair",
        ),
        db.UniqueConstraint(
            "external_provider",
            "external_reference",
            name="uq_payment_external_reference",
        ),
        db.Index("ix_payment_booking_recorded", "booking_id", "recorded_at"),
    )

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(
        db.String(20), nullable=False, default=PaymentStatus.UNPAID.value
    )
    external_provider = db.Column(db.String(50), nullable=True)
    external_reference = db.Column(db.String(120), nullable=True)
    recorded_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    booking = db.relationship("Booking", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.id}: booking={self.booking_id} status={self.status}>"
