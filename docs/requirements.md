# Requirements

## User Requirements
- Staff can add and view guest records with contact details.
- Staff can add rooms and update room status.
- Staff can create and manage bookings.
- Staff can check guests in and out.
- Staff can see room availability and booking activity from a dashboard.

## System Requirements
- Python Flask web application.
- Flask-SQLAlchemy ORM.
- SQLite database.
- Jinja2 template rendering.
- Bootstrap responsive interface.
- Booking validation for required fields, valid date ranges and overlap prevention.

## MVP Scope
- Single staff-facing interface (no authentication in MVP).
- Management of 10 seeded rooms.
- Guest, room and booking CRUD-lite workflows.
- Booking status workflow: Pending, Confirmed, Checked-in, Checked-out, Cancelled.
- Room status workflow: Available, Occupied, Cleaning, Maintenance.
