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
| Backend | Python Flask | Handles routes, form submissions and application workflow |
| Service layer | Python service modules | Contains reusable booking rules, validation and notification logic |
| Database ORM | Flask-SQLAlchemy | Maps Python classes to database tables |
| Database | SQLite | Stores local prototype data |
| Templates | Jinja2 | Renders dynamic HTML pages |
| Styling | Bootstrap and custom CSS | Provides responsive layout and visual styling |
| Frontend behaviour | Vanilla JavaScript | Adds lightweight validation, filtering and confirmation |
| Testing | pytest | Provides automated unit and integration testing |
| Version control | Git and GitHub | Tracks changes, branches and pull requests |
| Documentation | Markdown | Records requirements, testing, user guidance and technical notes |

---

## Architecture Summary

The application follows a lightweight layered Flask architecture inspired by the Model-View-Controller pattern.

The main components are:

- **Models:** stored in `models.py`; define database entities such as Guest, Room, Booking and NotificationLog.
- **Views/Templates:** stored in the `templates/` folder; provide the browser-based interface for staff users.
- **Application Routes:** stored in `app.py`; handle HTTP requests, render templates and coordinate application workflows.
- **Service Layer:** stored in the `services/` folder; contains reusable business logic, validation rules and notification operations.
- **Static Assets:** stored in `static/`; contain CSS and JavaScript files used for interface improvements.
- **Tests:** stored in the `tests/` folder; verify booking rules, notifications, Telegram commands and protected API behaviour.

The separation of business logic into dedicated service modules improves maintainability, reduces duplication and allows important rules to be tested independently from the web routes.

---

## Project Structure

The main source-controlled project structure is:

```text
boutique-hotel-booking-system/
├── .env.example
├── .gitignore
├── app.py
├── models.py
├── telegram_bot_worker.py
├── requirements.txt
├── README.md
├── LICENSE
├── services/
│   ├── __init__.py
│   ├── booking_service.py
│   ├── email_service.py
│   ├── notification_service.py
│   ├── telegram_command_service.py
│   └── telegram_service.py
├── templates/
│   ├── add_booking.html
│   ├── add_guest.html
│   ├── add_room.html
│   ├── base.html
│   ├── bookings.html
│   ├── dashboard.html
│   ├── guests.html
│   ├── notifications.html
│   └── rooms.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── tests/
│   ├── conftest.py
│   ├── test_booking_service.py
│   ├── test_checkout_notifications.py
│   ├── test_notification_service.py
│   └── test_telegram_command_service.py
├── docs/
│   ├── api-design-diagrams.md
│   ├── api-integration-overview.md
│   ├── data-security-report.md
│   ├── design-diagrams.md
│   ├── development-log.md
│   ├── email-notification-workflow.md
│   ├── notification-workflow-design.md
│   ├── peer-review.md
│   ├── requirements.md
│   ├── technical-notes.md
│   ├── telegram-staff-bot-workflow.md
│   ├── test-results-template.md
│   ├── testing-plan.md
│   ├── traceability-matrix.md
│   └── user-guide.md
└── screenshots/
    ├── .gitkeep
    ├── 01-dashboard.png
    ├── 02-rooms-page.png
    ├── 04-room-filter.png
    ├── 05-guests-page.png
    ├── 09-add-booking-form.png
    ├── 13-bookings-page.png
    └── 14-booking-filter.png
```

The project uses a layered structure where Flask routes coordinate application workflows, service modules contain reusable business logic, models define database entities, and the tests folder contains automated pytest coverage.

Local and machine-specific files such as `.env`, `.DS_Store`, the virtual environment, cache folders and runtime database files are not included in the documented source-controlled structure. These files should not be committed to GitHub.

The `.env.example` file documents the required environment variable names without exposing real credentials.

---

## Backend Design

The backend is built with Flask. Its route-level responsibilities include:

- defining URL routes;
- rendering templates;
- handling form submissions;
- validating required form values;
- coordinating application workflows;
- creating and updating database records;
- displaying success, warning and validation messages;
- delegating reusable booking rules to the service layer.

The main backend file is:

```text
app.py
```

Important backend workflows include:

- adding guests;
- adding rooms;
- creating bookings;
- cancelling bookings;
- checking guests in;
- checking guests out;
- updating room status;
- displaying notification records.

---

## Service Layer Design

The project includes a dedicated service layer to separate reusable business logic from Flask route handling.

The main booking service module is:

```text
services/booking_service.py
```

The booking service provides reusable functions for:

- validating booking requests;
- creating bookings;
- calculating booking prices;
- preventing overlapping bookings;
- blocking bookings for maintenance rooms;
- cancelling eligible bookings;
- applying check-in state transitions;
- applying check-out state transitions.

The service functions modify the relevant SQLAlchemy objects but do not commit database transactions. Transaction control remains in the application routes, allowing routes to commit successful operations or roll back failed operations.

The existing notification service modules remain responsible for Telegram delivery, email fallback and notification workflow behaviour.

---

## Database Design

The database layer uses Flask-SQLAlchemy with SQLite.

The main entities are:

| Entity | Purpose |
|---|---|
| Guest | Stores guest contact information |
| Room | Stores room number, room type, price and availability status |
| Booking | Stores guest-room booking records, dates, status and total price |
| NotificationLog | Stores notification delivery results, communication channel status and audit information |

### Relationships

- One Guest can have many Bookings.
- One Room can have many Bookings.
- Each Booking belongs to one Guest and one Room.
- One Room can be linked to many NotificationLog records.
- One Booking can be linked to many NotificationLog records.
- A NotificationLog may reference a Room and may optionally reference a Booking.

### Main database models

```text
Guest
Room
Booking
NotificationLog
```

This data model supports the core hotel workflow and records notification delivery evidence without requiring a complex production database design.

---

## Business Logic

The application includes business rules that reduce operational risk.

### Booking date validation

The system checks that the check-out date is after the check-in date. This prevents invalid bookings with zero or negative stay duration.

### Booking status validation

New bookings can only be created with the status `Pending` or `Confirmed`. This prevents users from bypassing the normal booking lifecycle.

### Overlapping booking validation

The system checks whether the selected room already has an active booking during the requested date range. Active booking statuses include:

```text
Pending
Confirmed
Checked-in
```

This reduces the risk of double bookings. Adjacent bookings remain valid when one booking starts on the date that the previous booking ends.

### Maintenance room prevention

The system prevents bookings for rooms marked as `Maintenance`. This helps avoid assigning guests to rooms that are not usable.

### Booking cancellation

Bookings can be cancelled unless they are already `Checked-out` or `Cancelled`.

### Check-in workflow

When an eligible booking is checked in:

- the booking status becomes `Checked-in`;
- the room status becomes `Occupied`.

The system also prevents check-in before the booking’s scheduled check-in date.

### Check-out workflow

When a checked-in booking is checked out:

- the booking status becomes `Checked-out`;
- the room status becomes `Cleaning`.

The existing notification workflow then attempts to inform housekeeping and stores the delivery result in NotificationLog.

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
templates/notifications.html
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

No React, Vue, Angular, jQuery, TypeScript or frontend build tools are required.

---

## Validation Strategy

The system uses both client-side and server-side validation.

### Client-side validation

Client-side validation improves user experience by giving quick feedback before the form is submitted.

Examples include:

- checking that the check-out date is after the check-in date;
- requesting confirmation before booking cancellation.

### Server-side validation

Server-side validation protects data integrity and is more important than client-side validation.

Examples include:

- required fields must be completed;
- email addresses must have a basic valid format;
- duplicate guest email addresses are rejected;
- check-out dates must be after check-in dates;
- new bookings must use an allowed initial status;
- selected rooms must exist;
- selected rooms must not be under Maintenance;
- selected rooms must not have an overlapping active booking;
- check-in cannot occur before the scheduled date;
- booking lifecycle transitions must follow the defined rules.

This layered validation approach improves reliability because users cannot bypass critical rules by disabling JavaScript.

---

## Security and Data Considerations

The MVP is not a production system, but it still follows basic responsible design principles.

Current measures include:

- no hard-coded production API keys;
- environment variables used for secrets and API credentials;
- application startup blocked when `SECRET_KEY` is missing;
- API key protection for the internal notification JSON endpoint;
- no payment data stored;
- only operationally necessary guest data stored;
- data-minimised housekeeping notifications;
- SQLite database kept local for the academic MVP;
- `.gitignore` used to avoid committing runtime data, credentials and environment files.

Production improvements would include:

- role-based authentication;
- HTTPS deployment;
- stronger password and session security;
- PostgreSQL database;
- automated backups;
- wider audit logging;
- GDPR-focused retention policies;
- access control for receptionist, housekeeping and manager roles.

---

## Testing Approach

The MVP uses both automated testing and manual functional testing to verify that the application works correctly and that important business rules are enforced.

Automated testing is implemented using `pytest` and covers the main backend functionality, including:

- booking creation and price calculation;
- invalid booking date prevention;
- overlapping booking prevention;
- maintenance-room booking prevention;
- booking cancellation rules;
- guest check-in validation;
- room status updates during check-in and check-out;
- notification service behaviour;
- Telegram command handling;
- protected API endpoint access.

The current automated test suite successfully completes:

```text
34 passed
```

Manual functional testing is used to verify complete user workflows through the browser interface and to collect visual evidence.

Manual testing should cover:

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

- no full staff login or role-based access control;
- no guest editing workflow yet;
- no customer-facing booking portal;
- no online payment integration;
- no customer-facing booking confirmation email or SMS workflow;
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
6. Expand audit logging for booking and room status changes.
7. Add customer-facing booking confirmation emails.
8. Add a customer self-booking portal.
9. Add reporting charts for occupancy and revenue.
10. Expand automated coverage with additional route-level, integration and end-to-end tests.

---

## Technical Summary

The application uses a clear and appropriate technical stack for an academic web application prototype. Flask coordinates web requests, SQLAlchemy manages database interaction, SQLite stores local data, Jinja2 renders dynamic pages, Bootstrap and CSS provide presentation, and vanilla JavaScript improves usability.

Dedicated service modules separate reusable business rules and notification behaviour from route handling. Automated pytest coverage and manual workflow evidence support validation of the implemented functionality.

The design remains simple, explainable and appropriate for the project scope while providing realistic opportunities for future improvement.