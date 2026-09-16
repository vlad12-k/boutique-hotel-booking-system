import secrets
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import DBAPIError

from hotel_app.extensions import limiter
from hotel_app.models import (
    ACTIVE_BOOKING_STATUSES,
    BOOKING_SOURCES,
    BOOKING_STATUSES,
    ROOM_STATUSES,
    Booking,
    Guest,
    NotificationLog,
    Room,
    RoomType,
    db,
)
from hotel_app.security import is_valid_email


from services.booking_service import (
    BookingServiceError,
    cancel_booking as cancel_booking_service,
    check_in_booking as check_in_booking_service,
    check_out_booking as check_out_booking_service,
    create_booking,
    is_availability_conflict,
    is_external_reference_conflict,
)
from services.notification_service import (
    send_housekeeping_notification,
    send_room_ready_notification,
)


def require_api_key(view_func):
    """Protects internal JSON API endpoints with a simple API key."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        expected_key = current_app.config.get("API_ADMIN_TOKEN")
        provided_key = request.headers.get("X-API-Key")

        if (
            not expected_key
            or not provided_key
            or not secrets.compare_digest(
                str(expected_key),
                str(provided_key),
            )
        ):
            return jsonify({"error": "Unauthorised"}), 401

        return view_func(*args, **kwargs)

    return wrapper


def api_limit() -> str:
    return current_app.config["API_RATE_LIMIT"]


def render_add_booking_form(guests_list, rooms_list):
    return render_template(
        "add_booking.html",
        guests=guests_list,
        rooms=rooms_list,
        booking_statuses=BOOKING_STATUSES,
        booking_sources=BOOKING_SOURCES,
    )


def parse_form_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def register_routes(app):
    @app.route("/")
    @login_required
    def dashboard():
        today = date.today()

        all_rooms = Room.query.all()
        room_statuses = [room.status for room in all_rooms]
        total_rooms = len(all_rooms)
        available_rooms = room_statuses.count("Available")
        occupied_rooms = room_statuses.count("Occupied")
        cleaning_rooms = room_statuses.count("Cleaning")
        maintenance_rooms = room_statuses.count("Maintenance")

        todays_check_ins = (
            Booking.query.filter(
                Booking.check_in_date == today,
                Booking.status.in_(ACTIVE_BOOKING_STATUSES),
            )
            .order_by(Booking.check_in_date.asc())
            .all()
        )

        todays_check_outs = (
            Booking.query.filter(
                Booking.check_out_date == today,
                Booking.status.in_(["Confirmed", "Checked-in", "Checked-out"]),
            )
            .order_by(Booking.check_out_date.asc())
            .all()
        )

        recent_bookings = (
            Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
        )

        return render_template(
            "dashboard.html",
            total_rooms=total_rooms,
            available_rooms=available_rooms,
            occupied_rooms=occupied_rooms,
            cleaning_rooms=cleaning_rooms,
            maintenance_rooms=maintenance_rooms,
            todays_check_ins=todays_check_ins,
            todays_check_outs=todays_check_outs,
            recent_bookings=recent_bookings,
        )

    @app.route("/rooms")
    @login_required
    def rooms():
        rooms_list = Room.query.order_by(Room.room_number.asc()).all()

        return render_template(
            "rooms.html",
            rooms=rooms_list,
            room_statuses=ROOM_STATUSES,
        )

    @app.route("/rooms/add", methods=["GET", "POST"])
    @login_required
    def add_room():
        room_types = RoomType.query.filter_by(is_active=True).order_by(
            RoomType.display_name.asc()
        ).all()
        if request.method == "POST":
            room_number = request.form.get("room_number", "").strip()
            room_type_id = request.form.get("room_type_id", "").strip()
            legacy_room_type_label = request.form.get("room_type", "").strip()
            price_per_night = request.form.get("price_per_night", "").strip()
            status = request.form.get("status", "Available").strip()

            if (
                not room_number
                or not (room_type_id or legacy_room_type_label)
                or not price_per_night
            ):
                flash(
                    "Room number, room type and price are required.",
                    "danger",
                )
                return render_template(
                    "add_room.html",
                    room_statuses=ROOM_STATUSES,
                    room_types=room_types,
                    currency=current_app.config["PROPERTY_CURRENCY"],
                )

            try:
                price_value = Decimal(price_per_night).quantize(Decimal("0.01"))

                if price_value <= 0:
                    raise InvalidOperation
                if room_type_id:
                    selected_room_type = db.session.get(RoomType, int(room_type_id))
                    if selected_room_type is None or not selected_room_type.is_active:
                        raise ValueError
                else:
                    selected_room_type = RoomType.query.filter_by(
                        display_name=legacy_room_type_label,
                        is_active=True,
                    ).first()
                    if selected_room_type is None:
                        selected_room_type = RoomType(
                            code=f"manual-{secrets.token_hex(8)}",
                            display_name=legacy_room_type_label,
                            bathroom_type="unspecified",
                        )
                        db.session.add(selected_room_type)
            except (InvalidOperation, ValueError):
                flash(
                    "Price per night must be a positive number.",
                    "danger",
                )
                return render_template(
                    "add_room.html",
                    room_statuses=ROOM_STATUSES,
                    room_types=room_types,
                    currency=current_app.config["PROPERTY_CURRENCY"],
                )

            if status not in ROOM_STATUSES:
                flash("Invalid room status.", "danger")
                return render_template(
                    "add_room.html",
                    room_statuses=ROOM_STATUSES,
                    room_types=room_types,
                    currency=current_app.config["PROPERTY_CURRENCY"],
                )

            if Room.query.filter_by(room_number=room_number).first():
                flash("Room number already exists.", "danger")
                return render_template(
                    "add_room.html",
                    room_statuses=ROOM_STATUSES,
                    room_types=room_types,
                    currency=current_app.config["PROPERTY_CURRENCY"],
                )

            db.session.add(
                Room(
                    room_number=room_number,
                    room_type=selected_room_type,
                    price_per_night=price_value,
                    currency=current_app.config["PROPERTY_CURRENCY"],
                    status=status,
                )
            )

            db.session.commit()
            flash("Room added successfully.", "success")
            return redirect(url_for("rooms"))

        return render_template(
            "add_room.html",
            room_statuses=ROOM_STATUSES,
            room_types=room_types,
            currency=current_app.config["PROPERTY_CURRENCY"],
        )

    @app.post("/rooms/<int:room_id>/status")
    @login_required
    def update_room_status(room_id):
        room = Room.query.get_or_404(room_id)
        previous_status = room.status
        status = request.form.get("status", "").strip()

        if status not in ROOM_STATUSES:
            flash("Invalid room status selected.", "danger")
            return redirect(url_for("rooms"))

        room.status = status

        if previous_status == "Cleaning" and status == "Available":
            notification_result = send_room_ready_notification(
                room,
                delivery_enabled=current_app.config[
                    "NOTIFICATION_DELIVERY_ENABLED"
                ],
            )

            notification_log = NotificationLog(
                room_id=room.id,
                booking_id=None,
                channel=notification_result["channel"],
                status="Sent" if notification_result["success"] else "Failed",
                message=notification_result["message"],
                error_message=notification_result["error"],
            )

            db.session.add(notification_log)

            if notification_result["success"]:
                flash(
                    f"Room status updated to Available. "
                    f"Room-ready notification sent via "
                    f"{notification_result['channel']}.",
                    "success",
                )
            else:
                flash(
                    "Room status updated to Available, but the room-ready "
                    "notification failed. Check notification logs.",
                    "warning",
                )
        else:
            flash("Room status updated.", "success")

        db.session.commit()
        return redirect(url_for("rooms"))

    @app.route("/guests")
    @login_required
    def guests():
        guests_list = Guest.query.order_by(Guest.full_name.asc()).all()

        return render_template(
            "guests.html",
            guests=guests_list,
        )

    @app.route("/guests/add", methods=["GET", "POST"])
    @login_required
    def add_guest():
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            notes = request.form.get("notes", "").strip()

            if not full_name:
                flash(
                    "Full name is required.",
                    "danger",
                )
                return render_template("add_guest.html")

            email = email.lower() or None
            phone = phone or None

            if email and not is_valid_email(email):
                flash(
                    "Please enter a valid email address.",
                    "danger",
                )
                return render_template("add_guest.html")

            if email and Guest.query.filter(Guest.email.ilike(email)).first():
                flash(
                    "A guest with this email address already exists.",
                    "danger",
                )
                return render_template("add_guest.html")

            db.session.add(
                Guest(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    notes=notes,
                )
            )

            db.session.commit()
            flash("Guest added successfully.", "success")
            return redirect(url_for("guests"))

        return render_template("add_guest.html")

    @app.route("/bookings")
    @login_required
    def bookings():
        bookings_list = Booking.query.order_by(
            Booking.created_at.desc()
        ).all()

        return render_template(
            "bookings.html",
            bookings=bookings_list,
        )

    @app.route("/bookings/add", methods=["GET", "POST"])
    @login_required
    def add_booking():
        guests_list = Guest.query.order_by(Guest.full_name.asc()).all()
        rooms_list = Room.query.order_by(Room.room_number.asc()).all()

        if request.method == "POST":
            guest_id = request.form.get("guest_id", "").strip()
            room_id = request.form.get("room_id", "").strip()
            check_in_date = parse_form_date(
                request.form.get("check_in_date")
            )
            check_out_date = parse_form_date(
                request.form.get("check_out_date")
            )
            booking_status = request.form.get(
                "status",
                "Confirmed",
            ).strip()
            source = request.form.get("source", "direct").strip()
            external_provider = request.form.get("external_provider", "").strip()
            external_reference = request.form.get("external_reference", "").strip()

            if (
                not guest_id
                or not room_id
                or not check_in_date
                or not check_out_date
            ):
                flash(
                    "Guest, room, check-in date and check-out date are required.",
                    "danger",
                )
                return render_add_booking_form(
                    guests_list,
                    rooms_list,
                )

            try:
                create_booking(
                    guest_id=int(guest_id),
                    room_id=int(room_id),
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    booking_status=booking_status,
                    source=source,
                    external_provider=external_provider or None,
                    external_reference=external_reference or None,
                    actor_staff_account_id=current_user.id,
                )

                db.session.commit()

            except ValueError:
                db.session.rollback()
                flash(
                    "Please select a valid guest and room.",
                    "danger",
                )
                return render_add_booking_form(
                    guests_list,
                    rooms_list,
                )

            except BookingServiceError as error:
                db.session.rollback()
                flash(str(error), "danger")
                return render_add_booking_form(
                    guests_list,
                    rooms_list,
                )

            except DBAPIError as error:
                db.session.rollback()
                if is_availability_conflict(error):
                    flash(
                        "Booking rejected: the selected room is no longer available "
                        "for those dates.",
                        "danger",
                    )
                elif is_external_reference_conflict(error):
                    flash(
                        "This external reservation is already recorded.",
                        "danger",
                    )
                else:
                    raise
                return render_add_booking_form(guests_list, rooms_list)

            flash("Booking created successfully.", "success")
            return redirect(url_for("bookings"))

        return render_add_booking_form(
            guests_list,
            rooms_list,
        )

    @app.post("/bookings/<int:booking_id>/cancel")
    @login_required
    def cancel_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        try:
            cancel_booking_service(
                booking, actor_staff_account_id=current_user.id
            )
            db.session.commit()
        except BookingServiceError as error:
            db.session.rollback()
            flash(str(error), "danger")
            return redirect(url_for("bookings"))

        flash("Booking cancelled.", "success")
        return redirect(url_for("bookings"))

    @app.post("/bookings/<int:booking_id>/checkin")
    @login_required
    def check_in_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        try:
            check_in_booking_service(
                booking,
                current_date=date.today(),
                actor_staff_account_id=current_user.id,
            )
            db.session.commit()
        except BookingServiceError as error:
            db.session.rollback()
            flash(str(error), "danger")
            return redirect(url_for("bookings"))

        flash("Guest checked in successfully.", "success")
        return redirect(url_for("bookings"))

    @app.post("/bookings/<int:booking_id>/checkout")
    @login_required
    def check_out_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        if booking.status != "Checked-in":
            flash(
                "Only checked-in bookings can be checked out.",
                "danger",
            )
            return redirect(url_for("bookings"))

        check_out_booking_service(
            booking, actor_staff_account_id=current_user.id
        )

        notification_result = send_housekeeping_notification(
            booking.room,
            booking,
            delivery_enabled=current_app.config[
                "NOTIFICATION_DELIVERY_ENABLED"
            ],
        )

        notification_log = NotificationLog(
            room_id=booking.room.id,
            booking_id=booking.id,
            channel=notification_result["channel"],
            status="Sent" if notification_result["success"] else "Failed",
            message=notification_result["message"],
            error_message=notification_result["error"],
        )

        db.session.add(notification_log)
        db.session.commit()

        if notification_result["success"]:
            flash(
                f"Guest checked out. Room moved to Cleaning. "
                f"Housekeeping notification sent via "
                f"{notification_result['channel']}.",
                "success",
            )
        else:
            flash(
                "Guest checked out and room moved to Cleaning, but "
                "housekeeping notification failed. Check notification logs.",
                "warning",
            )

        return redirect(url_for("bookings"))

    @app.get("/notifications")
    @login_required
    def notifications():
        logs = (
            NotificationLog.query
            .order_by(NotificationLog.created_at.desc())
            .all()
        )

        return render_template(
            "notifications.html",
            logs=logs,
        )

    @app.get("/api/notifications")
    @limiter.limit(api_limit)
    @require_api_key
    def api_notifications():
        logs = (
            NotificationLog.query
            .order_by(NotificationLog.created_at.desc())
            .all()
        )

        return jsonify(
            [
                {
                    "id": log.id,
                    "room_id": log.room_id,
                    "booking_id": log.booking_id,
                    "room_number": (
                        log.room.room_number
                        if log.room
                        else None
                    ),
                    "channel": log.channel,
                    "status": log.status,
                    "message": log.message,
                    "error_message": log.error_message,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ]
        )

    @app.get("/api/health")
    def api_health():
        return jsonify(
            {
                "status": "ok",
                "service": "boutique-hotel-booking-system",
                "features": [
                    "room-management",
                    "booking-management",
                    "housekeeping-notifications",
                    "room-ready-notifications",
                    "notification-logging",
                ],
            }
        )
