

# Technical Notes

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This document explains the technical structure, implementation choices and main components of the Boutique Hotel Booking and Room Management System. It supports the Unit 36 development portfolio by showing how the application was built, which tools were used and how the technical design supports the business requirements.

---

## System Overview

The application is a staff-facing web system for a small 10-room boutique hotel. It allows hotel staff to manage rooms, guests and bookings through a simple browser-based interface.

The system is designed as an academic MVP rather than a production deployment. It focuses on demonstrating clear application structure, working business logic, validation, documentation and testing evidence.

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python Flask | Handles routes, form submissions and business logic |
| Database ORM | Flask-SQLAlchemy | Maps Python classes to database tables |
| Database | SQLite | Stores local prototype data |
| Templates | Jinja2 | Renders dynamic HTML pages |
| Styling | Bootstrap and custom CSS | Provides responsive layout and visual styling |
| Frontend behaviour | Vanilla JavaScript | Adds lightweight validation, filtering and confirmation |
| Version control | Git and GitHub | Tracks changes, branches and pull requests |
| Documentation | Markdown | Records requirements, testing, user guide and technical notes |

---

## Architecture Summary

The application follows a simple Model-View-Controller style structure:

- **Models:** stored in `models.py`; define Guest, Room and Booking entities.
- **Views/Templates:** stored in the `templates/` folder; display pages to the user.
- **Controller/Routes:** stored in `app.py`; handle requests, validation and database actions.
- **Static assets:** stored in `static/`; include CSS and JavaScript.

This structure is suitable for a small Flask project because it keeps the main responsibilities clear and easy to explain in the report.

---

## Project Structure

```text
boutique-hotel-booking-system/
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── LICENSE
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── rooms.html
│   ├── guests.html
│   ├── bookings.html
│   ├── add_room.html
│   ├── add_guest.html
│   └── add_booking.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── docs/
├── screenshots/
└── instance/
```

The `instance/` folder is used for the local SQLite database. It should not be committed to GitHub because it contains runtime data rather than source code.

---

## Backend Design

The backend is built with Flask. The main backend responsibilities are:

- defining URL routes;
- rendering templates;
- handling form submissions;
- validating user input;
- creating and updating database records;
- enforcing booking rules;
- updating room and booking statuses.

The main backend file is:

```text
app.py
```

Important backend workflows include:

- add guest;
- add room;
- add booking;
- cancel booking;
- check-in;
- check-out;
- update room status.

---

## Database Design

The database layer uses Flask-SQLAlchemy with SQLite.

The main entities are:

| Entity | Purpose |
|---|---|
| Guest | Stores guest contact information |
| Room | Stores room number, room type, price and status |
| Booking | Stores guest-room booking records, dates, status and total price |

### Relationships

- One Guest can have many Bookings.
- One Room can have many Bookings.
- Each Booking belongs to one Guest and one Room.

### Main database models

```text
Guest
Room
Booking
```

This data model is sufficient for the MVP because the hotel only needs to manage guest records, rooms and booking activity.

---

## Business Logic

The application includes business rules that reduce operational risk.

### Booking date validation

The system checks that the check-out date is after the check-in date. This prevents invalid bookings with zero or negative stay duration.

### Overlapping booking validation

The system checks whether the selected room already has an active booking during the requested date range. Active booking statuses include:

```text
Pending
Confirmed
Checked-in
```

This reduces the risk of double bookings.

### Maintenance room prevention

The system prevents bookings for rooms marked as Maintenance. This helps avoid assigning guests to rooms that are not usable.

### Check-in workflow

When a booking is checked in:

- booking status becomes `Checked-in`;
- room status becomes `Occupied`.

### Check-out workflow

When a booking is checked out:

- booking status becomes `Checked-out`;
- room status becomes `Cleaning`.

This supports coordination between reception and housekeeping.

---

## Frontend Design

The frontend uses Jinja2 templates, Bootstrap, custom CSS and vanilla JavaScript.

### Templates

The main shared layout is:

```text
templates/base.html
```

The main pages are:

```text
templates/dashboard.html
templates/rooms.html
templates/guests.html
templates/bookings.html
templates/add_guest.html
templates/add_room.html
templates/add_booking.html
```

### Styling

Styling is handled by:

```text
static/css/style.css
```

Bootstrap provides layout and components, while the custom stylesheet improves project-specific presentation.

---

## Vanilla JavaScript

The frontend interaction is handled by:

```text
static/js/app.js
```

The project intentionally uses vanilla JavaScript rather than a frontend framework. This keeps the prototype lightweight and aligns with the requirement for simple web technologies.

JavaScript is used for:

- room status filtering;
- booking status filtering;
- booking date validation before form submission;
- cancellation confirmation;
- filter empty-state messages.

The JavaScript uses plain browser APIs such as:

```text
document.addEventListener
getElementById
querySelectorAll
addEventListener
classList.toggle
window.confirm
```

No React, Vue, Angular, jQuery, TypeScript or build tools are required.

---

## Validation Strategy

The system uses both client-side and server-side validation.

### Client-side validation

Client-side validation improves user experience by giving quick feedback before the form is submitted.

Examples:

- check-out date must be after check-in date;
- booking cancellation requires confirmation.

### Server-side validation

Server-side validation protects data integrity and is more important than client-side validation.

Examples:

- required fields must be completed;
- email address must have a basic valid format;
- check-out date must be after check-in date;
- selected room must not be under Maintenance;
- selected room must not already have an overlapping active booking.

This layered validation approach improves reliability because users cannot bypass critical rules by disabling JavaScript.

---

## Security and Data Considerations

The MVP is not a production system, but it still follows basic responsible design principles.

Current measures:

- no hard-coded production API keys;
- local development secret key fallback;
- no payment data stored;
- only operationally necessary guest data stored;
- SQLite database kept local;
- `.gitignore` used to avoid committing runtime and environment files.

Production improvements would include:

- role-based authentication;
- HTTPS deployment;
- stronger password and session security;
- PostgreSQL database;
- automated backups;
- audit logging;
- GDPR-focused retention policy;
- access control for reception, housekeeping and manager roles.

---

## Testing Approach

The MVP is tested using manual functional testing. Manual testing is suitable at this stage because the project is small and focused on demonstrating core workflows.

Testing should cover:

- dashboard loading;
- 10 seeded rooms displaying correctly;
- guest creation;
- invalid guest email validation;
- room status updates;
- valid booking creation;
- invalid booking date prevention;
- overlapping booking prevention;
- maintenance-room booking prevention;
- check-in workflow;
- check-out workflow;
- room filtering;
- booking filtering;
- cancellation confirmation.

Test evidence should be recorded in:

```text
docs/test-results-template.md
screenshots/
```

---

## Known Limitations

The current MVP has some limitations:

- no login or role-based access control;
- no guest editing workflow yet;
- no customer-facing booking portal;
- no online payments;
- no email or SMS confirmations;
- no cloud deployment;
- no automated backup process;
- no advanced reporting dashboard;
- SQLite is used instead of a production-grade database.

These limitations are acceptable for the MVP and can be discussed as future development opportunities in the evaluation chapter.

---

## Future Technical Improvements

Recommended future improvements include:

1. Add role-based login for receptionist, housekeeping and manager users.
2. Add Edit Guest functionality.
3. Migrate from SQLite to PostgreSQL for production readiness.
4. Deploy the application to a cloud platform.
5. Add automated database backups.
6. Add audit logs for booking and room status changes.
7. Add email confirmations for bookings.
8. Add a customer self-booking portal.
9. Add reporting charts for occupancy and revenue.
10. Add automated tests using pytest.

---

## Technical Summary

The application uses a clear and appropriate technical stack for an academic web application prototype. Flask provides the backend, SQLAlchemy manages database interaction, SQLite stores local data, Jinja2 renders dynamic pages, Bootstrap and CSS provide presentation, and vanilla JavaScript improves usability.

The design is simple, explainable and suitable for the project scope. It meets the main requirements while leaving realistic opportunities for future improvement.