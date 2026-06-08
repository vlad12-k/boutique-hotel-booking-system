import os
import secrets
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from models import (
    ACTIVE_BOOKING_STATUSES,
    BOOKING_STATUSES,
    ROOM_STATUSES,
    Booking,
    Guest,
    Room,
    db,
)


DEFAULT_ROOMS = [
    ("101", "Single", 70.0),
    ("102", "Single", 70.0),
    ("103", "Double", 95.0),
    ("104", "Double", 95.0),
    ("105", "Twin", 90.0),
    ("106", "Twin", 90.0),
    ("107", "Deluxe", 130.0),
    ("108", "Deluxe", 130.0),
    ("109", "Suite", 180.0),
    ("110", "Suite", 180.0),
]


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hotel.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_rooms()

    register_routes(app)
    return app


def seed_rooms():
    if Room.query.count() > 0:
        return

    rooms = [
        Room(room_number=number, room_type=room_type, price_per_night=price, status="Available")
        for number, room_type, price in DEFAULT_ROOMS
    ]
    db.session.add_all(rooms)
    db.session.commit()


def parse_form_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def register_routes(app):
    @app.route("/")
    def dashboard():
        today = date.today()
        total_rooms = Room.query.count()
        available_rooms = Room.query.filter_by(status="Available").count()
        occupied_rooms = Room.query.filter_by(status="Occupied").count()
        cleaning_rooms = Room.query.filter_by(status="Cleaning").count()
        maintenance_rooms = Room.query.filter_by(status="Maintenance").count()

        todays_check_ins = (
            Booking.query.filter(Booking.check_in_date == today, Booking.status.in_(ACTIVE_BOOKING_STATUSES))
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
        recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()

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
    def rooms():
        return render_template("rooms.html", rooms=Room.query.order_by(Room.room_number.asc()).all(), room_statuses=ROOM_STATUSES)

    @app.route("/rooms/add", methods=["GET", "POST"])
    def add_room():
        if request.method == "POST":
            room_number = request.form.get("room_number", "").strip()
            room_type = request.form.get("room_type", "").strip()
            price_per_night = request.form.get("price_per_night", "").strip()
            status = request.form.get("status", "Available").strip()

            if not room_number or not room_type or not price_per_night:
                flash("Room number, room type and price are required.", "danger")
                return render_template("add_room.html", room_statuses=ROOM_STATUSES)

            try:
                price_value = float(price_per_night)
                if price_value <= 0:
                    raise ValueError
            except ValueError:
                flash("Price per night must be a positive number.", "danger")
                return render_template("add_room.html", room_statuses=ROOM_STATUSES)

            if status not in ROOM_STATUSES:
                flash("Invalid room status.", "danger")
                return render_template("add_room.html", room_statuses=ROOM_STATUSES)

            if Room.query.filter_by(room_number=room_number).first():
                flash("Room number already exists.", "danger")
                return render_template("add_room.html", room_statuses=ROOM_STATUSES)

            db.session.add(
                Room(
                    room_number=room_number,
                    room_type=room_type,
                    price_per_night=price_value,
                    status=status,
                )
            )
            db.session.commit()
            flash("Room added successfully.", "success")
            return redirect(url_for("rooms"))

        return render_template("add_room.html", room_statuses=ROOM_STATUSES)

    @app.post("/rooms/<int:room_id>/status")
    def update_room_status(room_id):
        room = Room.query.get_or_404(room_id)
        status = request.form.get("status", "").strip()
        if status not in ROOM_STATUSES:
            flash("Invalid room status selected.", "danger")
            return redirect(url_for("rooms"))

        room.status = status
        db.session.commit()
        flash("Room status updated.", "success")
        return redirect(url_for("rooms"))

    @app.route("/guests")
    def guests():
        return render_template("guests.html", guests=Guest.query.order_by(Guest.full_name.asc()).all())

    @app.route("/guests/add", methods=["GET", "POST"])
    def add_guest():
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            notes = request.form.get("notes", "").strip()

            if not full_name or not email or not phone:
                flash("Full name, email and phone are required.", "danger")
                return render_template("add_guest.html")

            db.session.add(Guest(full_name=full_name, email=email, phone=phone, notes=notes))
            db.session.commit()
            flash("Guest added successfully.", "success")
            return redirect(url_for("guests"))

        return render_template("add_guest.html")

    @app.route("/bookings")
    def bookings():
        bookings_list = Booking.query.order_by(Booking.created_at.desc()).all()
        return render_template("bookings.html", bookings=bookings_list)

    @app.route("/bookings/add", methods=["GET", "POST"])
    def add_booking():
        guests_list = Guest.query.order_by(Guest.full_name.asc()).all()
        rooms_list = Room.query.order_by(Room.room_number.asc()).all()

        if request.method == "POST":
            guest_id = request.form.get("guest_id", "").strip()
            room_id = request.form.get("room_id", "").strip()
            check_in_date = parse_form_date(request.form.get("check_in_date"))
            check_out_date = parse_form_date(request.form.get("check_out_date"))
            booking_status = request.form.get("status", "Confirmed").strip()

            if not guest_id or not room_id or not check_in_date or not check_out_date:
                flash("Guest, room, check-in date and check-out date are required.", "danger")
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            if check_out_date <= check_in_date:
                flash("Check-out date must be after check-in date.", "danger")
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            if booking_status not in ["Pending", "Confirmed"]:
                flash("New bookings can only be Pending or Confirmed.", "danger")
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            try:
                guest_id = int(guest_id)
                room_id = int(room_id)
            except ValueError:
                flash("Please select a valid guest and room.", "danger")
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            selected_room = db.session.get(Room, room_id)
            selected_guest = db.session.get(Guest, guest_id)

            if not selected_room or not selected_guest:
                flash("Please select a valid guest and room.", "danger")
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            if selected_room.status == "Maintenance":
                flash("Rooms under Maintenance cannot be booked.", "danger")
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            overlapping_booking = Booking.query.filter(
                Booking.room_id == selected_room.id,
                Booking.status.in_(ACTIVE_BOOKING_STATUSES),
                Booking.check_in_date < check_out_date,
                Booking.check_out_date > check_in_date,
            ).first()

            if overlapping_booking:
                flash(
                    "Booking rejected: the selected room already has an active booking for overlapping dates.",
                    "danger",
                )
                return render_template(
                    "add_booking.html",
                    guests=guests_list,
                    rooms=rooms_list,
                    booking_statuses=BOOKING_STATUSES,
                )

            total_nights = (check_out_date - check_in_date).days
            total_price = total_nights * selected_room.price_per_night

            db.session.add(
                Booking(
                    guest_id=selected_guest.id,
                    room_id=selected_room.id,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    status=booking_status,
                    total_price=total_price,
                )
            )
            db.session.commit()
            flash("Booking created successfully.", "success")
            return redirect(url_for("bookings"))

        return render_template(
            "add_booking.html",
            guests=guests_list,
            rooms=rooms_list,
            booking_statuses=BOOKING_STATUSES,
        )

    @app.post("/bookings/<int:booking_id>/cancel")
    def cancel_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if booking.status in ["Checked-out", "Cancelled"]:
            flash("Booking cannot be cancelled in its current status.", "danger")
            return redirect(url_for("bookings"))

        booking.status = "Cancelled"
        db.session.commit()
        flash("Booking cancelled.", "success")
        return redirect(url_for("bookings"))

    @app.post("/bookings/<int:booking_id>/checkin")
    def check_in_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        if booking.status not in ["Pending", "Confirmed"]:
            flash("Only Pending or Confirmed bookings can be checked in.", "danger")
            return redirect(url_for("bookings"))

        if date.today() < booking.check_in_date:
            flash("Guest cannot be checked in before the check-in date.", "danger")
            return redirect(url_for("bookings"))

        booking.status = "Checked-in"
        booking.room.status = "Occupied"
        db.session.commit()
        flash("Guest checked in successfully.", "success")
        return redirect(url_for("bookings"))

    @app.post("/bookings/<int:booking_id>/checkout")
    def check_out_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        if booking.status != "Checked-in":
            flash("Only checked-in bookings can be checked out.", "danger")
            return redirect(url_for("bookings"))

        booking.status = "Checked-out"
        booking.room.status = "Cleaning"
        db.session.commit()
        flash("Guest checked out. Room moved to Cleaning.", "success")
        return redirect(url_for("bookings"))


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
