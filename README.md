# Boutique Hotel Booking and Room Management System

A staff-facing hotel operations web application for a small 10-room boutique hotel. The system helps reception staff and managers manage guests, rooms, bookings, room readiness, check-ins and check-outs from one simple internal dashboard.

This project was developed as an academic prototype for **Unit 36: Application Development** and is also structured as a portfolio-ready Flask project.

---

## Project Overview

Small hotels often rely on spreadsheets, paper notes or disconnected tools to manage bookings and room status. This can create operational problems such as double bookings, unclear room availability, delayed housekeeping updates and limited management visibility.

This application provides a lightweight internal system that supports the core daily workflow of a boutique hotel:

1. add guest records;
2. manage room inventory and room status;
3. create room bookings;
4. prevent invalid and overlapping bookings;
5. check guests in and out;
6. update room readiness after departure;
7. view operational activity from a dashboard.

---

## Key Features

### Dashboard

- Room availability overview
- Total, available, occupied, cleaning and maintenance room counts
- Today's check-ins
- Today's check-outs
- Recent booking activity

### Room Management

- View all rooms
- Add new rooms
- Update room status
- Filter rooms by status using vanilla JavaScript
- Empty-state message when no rooms match the selected filter

Supported room statuses:

- Available
- Occupied
- Cleaning
- Maintenance

### Guest Management

- Add guest records
- View guest contact details
- Validate email format
- Prevent duplicate guest email addresses

### Booking Management

- Create bookings for existing guests and rooms
- View all bookings
- Cancel bookings with confirmation prompt
- Check guests in
- Check guests out
- Filter bookings by status using vanilla JavaScript

Supported booking statuses:

- Pending
- Confirmed
- Checked-in
- Checked-out
- Cancelled

### Validation and Business Rules

The application includes backend validation for important business rules:

- required fields must be completed;
- check-out date must be after check-in date;
- rooms under Maintenance cannot be booked;
- overlapping active bookings for the same room are rejected;
- guest email addresses must use a valid basic format;
- duplicate guest email addresses are rejected.

Frontend validation and usability enhancements are provided using vanilla JavaScript.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Templates | Jinja2 |
| Styling | Bootstrap, custom CSS |
| Frontend behaviour | Vanilla JavaScript |
| External APIs | Telegram Bot API, Mailtrap SMTP Sandbox |
| Version control | Git, GitHub |
| Documentation | Markdown |

---

## Project Structure

```text
boutique-hotel-booking-system/
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── LICENSE
├── services/
│   ├── telegram_service.py
│   ├── telegram_command_service.py
│   ├── email_service.py
│   └── notification_service.py
├── telegram_bot_worker.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── rooms.html
│   ├── guests.html
│   ├── bookings.html
│   ├── notifications.html
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

The `instance/` folder is used for the local SQLite database and should not be committed to GitHub.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd boutique-hotel-booking-system
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

macOS / Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open the local app in your browser:

```text
http://127.0.0.1:5000
```

---

## Environment Variables

Copy `.env.example` to `.env` before running live notification tests:

```bash
cp .env.example .env
```

The local `.env` file stores real credentials and must not be committed to GitHub. The `.env.example` file stores safe placeholder values for documentation and setup purposes.

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Recommended outside local prototype use so Flask sessions stay stable |
| `FLASK_DEBUG=1` | Enables local debug mode during development |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token used for housekeeping notifications and staff command replies |
| `TELEGRAM_CHAT_ID` | Telegram chat used for outbound housekeeping alerts |
| `TELEGRAM_ALLOWED_CHAT_IDS` | Authorised Telegram staff chat IDs for command bot access control |
| `TELEGRAM_POLL_INTERVAL_SECONDS` | Local worker polling interval for Telegram staff commands |
| `EMAIL_HOST` | Mailtrap SMTP host used for fallback email testing |
| `EMAIL_PORT` | Mailtrap SMTP port, such as `2525` |
| `EMAIL_USERNAME` | Mailtrap SMTP username |
| `EMAIL_PASSWORD` | Mailtrap SMTP password stored only in local `.env` |
| `EMAIL_FROM` | Sender address used in test email messages |
| `EMAIL_TO` | Recipient address used for captured housekeeping emails |

Local debug example:

```bash
export FLASK_DEBUG=1
python app.py
```

---

## Documentation

The `docs/` folder contains supporting academic and development evidence:

| File | Purpose |
|---|---|
| `docs/requirements.md` | User requirements, system requirements and MVP scope |
| `docs/development-log.md` | Development iterations and reflection |
| `docs/technical-notes.md` | Architecture, stack and technical explanation |
| `docs/testing-plan.md` | Manual testing plan and test cases |
| `docs/test-results-template.md` | Template for actual test results and screenshot evidence |
| `docs/traceability-matrix.md` | Links requirements to implemented features and evidence |
| `docs/user-guide.md` | Staff-facing guide for using the system |
| `docs/api-integration-overview.md` | API integration overview for Telegram, Mailtrap email fallback and JSON audit endpoints |
| `docs/notification-workflow-design.md` | Notification workflow design and fallback behaviour |
| `docs/telegram-staff-bot-workflow.md` | Two-way Telegram staff command bot workflow |
| `docs/email-notification-workflow.md` | Mailtrap SMTP email fallback testing workflow |
| `docs/data-security-report.md` | Credential handling, data minimisation and API security notes |
| `docs/peer-review.md` | Peer review feedback and planned improvements |

---

## Testing

Manual testing should be completed using the test cases in:

```text
docs/testing-plan.md
docs/test-results-template.md
```

Recommended evidence screenshots include:

- dashboard overview;
- room list;
- guest creation;
- invalid guest email validation;
- booking creation;
- invalid booking date validation;
- overlapping booking prevention;
- maintenance-room booking prevention;
- check-in result;
- check-out result;
- room filtering;
- booking filtering;
- cancel confirmation.

Additional API evidence screenshots should be collected for:

- Telegram housekeeping notification delivery;
- Telegram staff command bot responses;
- notification log records;
- JSON notification API records;
- Mailtrap SMTP fallback email delivery;
- automated test output for the notification services.

Screenshots should be saved in the `screenshots/` folder.

---


## API-Based Housekeeping Notification Extension

The application includes an API-based housekeeping notification workflow that extends the room operations process. When reception staff check out a guest, the system updates the booking status, moves the room to `Cleaning`, attempts to notify housekeeping through Telegram, uses Mailtrap SMTP email fallback if the primary channel fails, and records the final result in a notification log.

The extension also includes a two-way Telegram staff command bot. Authorised staff can send commands from Telegram to check room status, list rooms waiting for cleaning, mark rooms as ready, move rooms into maintenance and review recent notification logs.

### Notification Features

- Check-out-triggered housekeeping alerts
- Room-ready notifications when a room changes from `Cleaning` to `Available`
- Primary Telegram Bot API notification service
- Mailtrap SMTP Sandbox email fallback service
- Two-way Telegram staff command bot using long polling
- Authorised Telegram chat ID validation
- Staff-facing notification log page
- JSON endpoint for notification records: `/api/notifications`
- Service health endpoint: `/api/health`
- Environment-based credential management through `.env.example`
- Data-minimised notification messages that avoid guest personal details

### Notification Workflow

1. Reception staff check out a booking.
2. The booking status changes to `Checked-out`.
3. The room status changes to `Cleaning`.
4. The notification service builds a data-minimised housekeeping message.
5. The system attempts primary Telegram delivery.
6. If the primary Telegram channel fails, Mailtrap SMTP email fallback delivery is attempted.
7. The final result is stored in the notification log.
8. Staff can review notification outcomes through `/notifications` and `/api/notifications`.

### Telegram Staff Command Workflow

Run the Flask application in one terminal:

```bash
python app.py
```

Run the Telegram worker in a second terminal:

```bash
python telegram_bot_worker.py
```

Supported Telegram staff commands:

| Command | Purpose |
|---|---|
| `/help` | Show available commands |
| `/status` | Show a live room status summary |
| `/cleaning` | List rooms waiting for housekeeping |
| `/available` | List available rooms |
| `/ready <room number>` | Mark a cleaned room as `Available` |
| `/maintenance <room number>` | Mark a room as `Maintenance` |
| `/notifications` | Show recent notification log entries |

### Mailtrap Email Fallback Workflow

Mailtrap SMTP Sandbox is used as a safe email testing service. It captures fallback emails inside the Mailtrap inbox instead of sending them to real recipients, which makes it suitable for academic evidence and local API testing.

A fallback email is sent when the primary Telegram notification channel is unavailable. The notification log records the final channel as `email`, and `/api/notifications` exposes the same audit record as JSON.

### Notification Configuration

Copy `.env.example` to `.env` and provide the required Telegram and Mailtrap credentials for live delivery tests. The local `.env` file must remain outside version control. The application still records controlled failure logs if notification credentials are not configured, which supports safe testing without exposing secrets.

### API Testing Evidence

The project includes automated tests for the notification service, Telegram command handling and email fallback behaviour. These tests verify that housekeeping messages avoid guest personal data, Telegram command parsing works, and email fallback is used when the primary Telegram API raises an error.

---

## Current MVP Limitations

This is an academic MVP and not a production hotel management platform.

Current limitations:

- no role-based login;
- no customer-facing booking portal;
- no guest editing workflow yet;
- no online payment integration;
- no customer-facing email or SMS booking confirmations yet;
- no cloud deployment;
- no automated backups;
- SQLite is used instead of PostgreSQL.

---

## Future Improvements

Recommended future improvements:

- add receptionist, housekeeping and manager roles;
- add Edit Guest functionality;
- migrate from SQLite to PostgreSQL;
- deploy to a cloud platform;
- add automated backups;
- add customer-facing booking confirmation emails;
- add payment integration;
- add customer self-booking portal;
- add audit logs for booking and room status changes;
- add reporting charts for occupancy and revenue.

---

## Academic Note

This project was created for **Unit 36: Application Development and Unit 37: Application Program Interfaces** and extended with API integration evidence suitable for the API-focused unit work. It demonstrates application design, development, validation, testing evidence, support documentation, external service integration and evaluation opportunities.

The system intentionally uses a simple Flask, SQLite, Bootstrap and vanilla JavaScript stack so that the implementation remains understandable, explainable and suitable for academic demonstration.
