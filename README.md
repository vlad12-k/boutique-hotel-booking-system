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

## Optional Environment Variables

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Recommended outside local prototype use so Flask sessions stay stable |
| `FLASK_DEBUG=1` | Enables local debug mode during development |

Example:

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

Screenshots should be saved in the `screenshots/` folder.

---


## API-Based Housekeeping Notification Extension

The application includes an API-based housekeeping notification workflow that extends the check-out process. When reception staff check out a guest, the system updates the booking status, moves the room to cleaning status, attempts to notify housekeeping through a primary messaging API, uses backup email delivery if required, and records the result in a notification log.

### Notification Features

- Checkout-triggered housekeeping alerts
- Primary Telegram notification service
- Backup email notification service
- Staff-facing notification log page
- JSON endpoint for notification records: `/api/notifications`
- Service health endpoint: `/api/health`
- Environment-based credential management through `.env.example`
- Data-minimised notification messages that avoid guest personal details

### Notification Workflow

1. Reception staff check out a booking.
2. The booking status changes to `Checked-out`.
3. The room status changes to `Cleaning`.
4. The notification service builds a housekeeping message.
5. The system attempts primary Telegram delivery.
6. If the primary channel fails, backup email delivery is attempted.
7. The final result is stored in the notification log.
8. Staff can review notification outcomes through `/notifications`.

### Notification Configuration

Copy `.env.example` to `.env` and provide the required credentials for live delivery. The application still records controlled failure logs if notification credentials are not configured, which supports safe testing without exposing secrets.

### API Testing Evidence

The project includes automated tests for the notification service and API endpoints. These tests verify that the health endpoint returns service status, the notification endpoint returns JSON records, and housekeeping messages avoid guest personal data.

## Current MVP Limitations

This is an academic MVP and not a production hotel management platform.

Current limitations:

- no role-based login;
- no customer-facing booking portal;
- no guest editing workflow yet;
- no online payment integration;
- no email or SMS confirmations;
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
- add email confirmations;
- add payment integration;
- add customer self-booking portal;
- add audit logs for booking and room status changes;
- add reporting charts for occupancy and revenue.

---

## Academic Note

This project was created for **Unit 36: Application Development**. It demonstrates application design, development, validation, testing evidence, support documentation and evaluation opportunities.

The system intentionally uses a simple Flask, SQLite, Bootstrap and vanilla JavaScript stack so that the implementation remains understandable, explainable and suitable for academic demonstration.
