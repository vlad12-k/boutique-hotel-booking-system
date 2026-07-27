# Boutique Hotel Booking and Room Management System

A staff-facing Flask web application for managing guests, rooms, bookings, room readiness, check-ins and check-outs in a small boutique hotel.

The project contains:

- the core hotel-management application developed for **Unit 36: Application Development**;
- a later housekeeping-notification extension developed for **Unit 37: Application Program Interfaces**.

The two areas are documented separately so that the original application scope and the later API integration remain clear.

---

## Project Overview

Small hotels may rely on spreadsheets, paper notes or disconnected systems to manage bookings and room status. This can increase the risk of:

- overlapping bookings;
- incorrect booking dates;
- unavailable rooms being assigned;
- unclear room readiness;
- delayed housekeeping communication;
- limited visibility of daily activity.

The core application provides an internal system for managing:

- guest records;
- room records and operational status;
- validated bookings;
- check-in and check-out;
- booking cancellation;
- room and booking filtering;
- dashboard summaries.

The later notification extension adds Telegram housekeeping alerts, SMTP email fallback, a Telegram staff command worker and notification audit records.

---

## Core Application Features

### Dashboard

The dashboard displays:

- total rooms;
- available rooms;
- occupied rooms;
- rooms being cleaned;
- rooms under Maintenance;
- today’s check-ins;
- today’s check-outs;
- recent bookings.

### Room management

Staff can:

- view room records;
- add rooms;
- update room status;
- filter rooms by status.

Supported room statuses are:

- `Available`;
- `Occupied`;
- `Cleaning`;
- `Maintenance`.

### Guest management

Staff can:

- add guest records;
- view guest contact details;
- validate guest email format;
- prevent duplicate guest email records.

Editing existing guest records remains outside the current MVP.

### Booking management

Staff can:

- create bookings;
- view booking records;
- calculate total stay price;
- cancel eligible bookings;
- check guests in;
- check guests out;
- filter bookings by status.

Supported booking statuses are:

- `Pending`;
- `Confirmed`;
- `Checked-in`;
- `Checked-out`;
- `Cancelled`.

### Validation rules

The application enforces the following business rules:

- required booking information must be provided;
- check-out must be later than check-in;
- rooms under Maintenance cannot be booked;
- overlapping active bookings for the same room are rejected;
- guest email addresses must use a valid basic format;
- duplicate guest email records are rejected.

Critical rules are enforced on the server. Vanilla JavaScript provides additional frontend validation, filtering and cancellation confirmation.

---

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python and Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Templates | Jinja2 |
| Interface | Bootstrap and custom CSS |
| Frontend interaction | Vanilla JavaScript |
| Automated testing | pytest |
| Messaging integration | Telegram Bot API |
| Email fallback | SMTP using Mailtrap Sandbox |
| Configuration | Environment variables through `.env` |
| Version control | Git and GitHub |
| Documentation | Markdown and Mermaid |

---

## Repository Structure

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
│   ├── base.html
│   ├── dashboard.html
│   ├── rooms.html
│   ├── add_room.html
│   ├── guests.html
│   ├── add_guest.html
│   ├── bookings.html
│   ├── add_booking.html
│   └── notifications.html
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
│   ├── requirements.md
│   ├── design-diagrams.md
│   ├── development-log.md
│   ├── peer-review.md
│   ├── technical-notes.md
│   ├── testing-plan.md
│   ├── test-results-template.md
│   ├── traceability-matrix.md
│   ├── user-guide.md
│   ├── api-design-diagrams.md
│   ├── api-integration-overview.md
│   ├── notification-workflow-design.md
│   ├── telegram-staff-bot-workflow.md
│   ├── email-notification-workflow.md
│   └── data-security-report.md
└── screenshots/
```

The local `.env` file contains credentials and must not be committed. Runtime-generated files and operating-system metadata such as `.DS_Store` should also remain outside version control.

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd boutique-hotel-booking-system
```

Replace `<repository-url>` with the actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the environment

macOS or Linux:

```bash
source venv/bin/activate
```

Windows Command Prompt:

```bat
venv\Scripts\activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Core Application

Start the Flask application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The application opens on the Dashboard.

Detailed user instructions are provided in:

```text
docs/user-guide.md
```

---

## Environment Configuration

Copy the example configuration before running live notification tests:

```bash
cp .env.example .env
```

The `.env.example` file contains safe placeholders. Real credentials belong only in the local `.env` file.

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Flask session signing key |
| `FLASK_DEBUG` | Enables local Flask debug mode when set appropriately |
| `API_ADMIN_TOKEN` | Protects the internal notification audit endpoint |
| `TELEGRAM_BOT_TOKEN` | Authenticates requests to the Telegram Bot API |
| `TELEGRAM_CHAT_ID` | Receives outbound housekeeping notifications |
| `TELEGRAM_ALLOWED_CHAT_IDS` | Defines authorised Telegram staff chats |
| `TELEGRAM_POLL_INTERVAL_SECONDS` | Controls the local command-worker polling interval |
| `EMAIL_HOST` | SMTP host used for fallback email testing |
| `EMAIL_PORT` | SMTP port |
| `EMAIL_USERNAME` | SMTP account username |
| `EMAIL_PASSWORD` | SMTP account password |
| `EMAIL_FROM` | Sender address used in test messages |
| `EMAIL_TO` | Recipient address used for captured fallback messages |

Do not include real secrets in screenshots, documentation, commits or test output.

---

## Automated Testing

Run the complete regression suite with:

```bash
pytest -q
```

The suite covers:

- booking-service validation;
- booking-status behaviour;
- check-out notification workflow;
- primary and fallback notification handling;
- Telegram staff command parsing and authorisation;
- notification security behaviour.

The latest previously recorded result was:

```text
34 passed
```

The suite must be run again after all final code and documentation changes. The final result should be retained as submission evidence and updated if the collected test count changes.

Manual test planning and results are recorded separately:

```text
docs/testing-plan.md
docs/test-results-template.md
```

---

## Unit 37 Housekeeping Notification Extension

The later extension adds external communication to the original check-out and room-readiness workflows.

### Main features

- housekeeping alert after guest check-out;
- room-ready notification when a room moves from `Cleaning` to `Available`;
- primary Telegram delivery;
- SMTP email fallback;
- notification log page;
- protected notification JSON endpoint;
- Telegram staff command worker;
- authorised-chat validation;
- data-minimised notification content.

### Check-out notification flow

1. Staff check out an eligible booking.
2. The booking changes to `Checked-out`.
3. The room changes to `Cleaning`.
4. A data-minimised housekeeping message is created.
5. Telegram delivery is attempted.
6. Email fallback is attempted when required.
7. The outcome is recorded in the notification log.

Detailed behaviour is documented in:

- `docs/api-integration-overview.md`;
- `docs/notification-workflow-design.md`;
- `docs/email-notification-workflow.md`;
- `docs/data-security-report.md`.

---

## Telegram Staff Command Worker

Run the Flask application in one terminal:

```bash
python app.py
```

Run the Telegram worker in a second terminal:

```bash
python telegram_bot_worker.py
```

Supported commands include:

| Command | Purpose |
|---|---|
| `/help` | Display available commands |
| `/status` | Display a room-status summary |
| `/cleaning` | List rooms waiting for cleaning |
| `/available` | List rooms marked Available |
| `/ready <room number>` | Change a cleaned room to Available |
| `/maintenance <room number>` | Change a room to Maintenance |
| `/notifications` | Display recent notification records |

Only chat IDs configured through `TELEGRAM_ALLOWED_CHAT_IDS` should be permitted to execute staff commands.

Further details are provided in:

```text
docs/telegram-staff-bot-workflow.md
```

---

## Internal API Endpoints

The extension includes internal endpoints for health and audit evidence.

| Endpoint | Purpose |
|---|---|
| `/api/health` | Returns application or service health information |
| `/api/notifications` | Returns notification audit records |

The notification endpoint requires the configured administrative token in the `X-API-Key` header.

Example:

```bash
curl \
  -H "X-API-Key: your_api_admin_token" \
  http://127.0.0.1:5000/api/notifications
```

Requests without a valid key should be rejected.

---

## Documentation

### Unit 36: Application Development

| File | Purpose |
|---|---|
| `docs/requirements.md` | Defines requirements, scope, risks and acceptance criteria |
| `docs/design-diagrams.md` | Contains ERD, DFD, workflows, use cases and page plan |
| `docs/development-log.md` | Records development iterations and reflection |
| `docs/peer-review.md` | Records supplied model review and the response to feedback |
| `docs/technical-notes.md` | Explains architecture and implementation decisions |
| `docs/testing-plan.md` | Defines the planned testing approach |
| `docs/test-results-template.md` | Records actual test outcomes and evidence |
| `docs/traceability-matrix.md` | Connects requirements, implementation, tests and evidence |
| `docs/user-guide.md` | Explains how staff use the application |

### Unit 37: Application Program Interfaces

| File | Purpose |
|---|---|
| `docs/api-design-diagrams.md` | Shows API and notification-extension design |
| `docs/api-integration-overview.md` | Summarises external services and endpoints |
| `docs/notification-workflow-design.md` | Defines primary, fallback and logging behaviour |
| `docs/telegram-staff-bot-workflow.md` | Documents two-way Telegram staff commands |
| `docs/email-notification-workflow.md` | Documents SMTP fallback testing |
| `docs/data-security-report.md` | Explains credential protection, access control and data minimisation |

---

## Current Limitations

The project is an academic prototype rather than a production hotel-management platform.

Current limitations include:

- no complete staff authentication system;
- no role-based receptionist, housekeeping and manager permissions;
- no guest-record editing;
- no customer-facing booking portal;
- no online payment processing;
- no customer booking confirmations;
- no production cloud deployment;
- no automated backup process;
- SQLite rather than a production server database;
- no advanced occupancy or revenue analytics.

---

## Future Development

Appropriate future improvements include:

- staff authentication and role-based access control;
- Edit Guest functionality;
- PostgreSQL migration;
- cloud deployment;
- automated database backups;
- customer booking confirmation emails;
- online payment integration;
- customer self-booking;
- audit logs for booking and room-status changes;
- occupancy and revenue reporting.

---

## Academic Context

The core application was developed for **Unit 36: Application Development**.

The housekeeping notification, Telegram, SMTP fallback and internal API functionality form a later extension for **Unit 37: Application Program Interfaces**.

The project demonstrates:

- requirements analysis;
- relational data modelling;
- application design;
- Flask development;
- business-rule validation;
- manual and automated testing;
- traceability;
- user and technical documentation;
- external service integration;
- security and data-minimisation considerations.

The stack remains intentionally lightweight so that the implementation can be demonstrated, tested and explained clearly.