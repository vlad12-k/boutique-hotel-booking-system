# Requirements Specification

## Project

Boutique Hotel Booking and Room Management System

## Purpose

This document defines the user requirements, system requirements, functional requirements, non-functional requirements and MVP scope for the boutique hotel booking and room management application.

The document supports the Unit 36 design and development evidence by showing what the application was expected to achieve and how the implemented features address the original business problem.

The repository also contains a completed Unit 37 API-based housekeeping notification extension. That extension is identified separately so that it does not alter the original Unit 36 MVP scope.

---

## Business Context

The client is a small boutique hotel with 10 rooms. The hotel requires a simple internal web application to help staff manage guests, rooms and bookings more reliably than a paper-based or spreadsheet-based process.

Manual booking and room tracking can lead to:

- double bookings;
- unclear room availability;
- delayed room status updates;
- poor coordination between reception and housekeeping;
- limited visibility for hotel managers.

The proposed solution is a staff-facing web application that allows hotel staff to manage daily operations from one place.

---

## User Roles

| User Role | Description | Main Needs |
|---|---|---|
| Reception Staff | Staff responsible for guests, bookings, check-ins and check-outs | Create guest records, create bookings, check guests in and out, and view room availability |
| Housekeeping Staff | Staff responsible for room readiness | View room information and update operational room status |
| Hotel Manager | Person responsible for operational oversight | View dashboard summaries and monitor booking and room activity |

The MVP uses a single staff-facing interface and does not include authentication or technical role-based access control. The roles describe expected operational users rather than separate authenticated account types.

Role-based authentication and permissions are identified as future improvements.

---

## User Requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| UR1 | Staff must be able to add and view guest records with contact details. | High | Implemented |
| UR2 | Staff must be able to add rooms and view the list of hotel rooms. | High | Implemented |
| UR3 | Staff must be able to update room status. | High | Implemented |
| UR4 | Staff must be able to create and manage bookings. | High | Implemented |
| UR5 | Staff must be able to check guests in and out. | High | Implemented |
| UR6 | Staff must be able to see room availability from the dashboard and rooms page. | High | Implemented |
| UR7 | Managers must be able to view booking activity and room status summaries. | Medium | Implemented |
| UR8 | Staff should be able to filter rooms and bookings by status. | Medium | Implemented |
| UR9 | Staff should receive clear validation feedback when booking data is invalid. | High | Implemented |
| UR10 | Staff should be able to edit guest records when contact details are entered incorrectly. | Medium | Planned improvement |

---

## System Requirements

| ID | Requirement | Implementation Evidence | Status |
|---|---|---|---|
| SR1 | The system shall be implemented as a Python Flask web application. | `app.py` | Implemented |
| SR2 | The system shall use Flask-SQLAlchemy as the object-relational mapper. | `models.py` | Implemented |
| SR3 | The system shall use SQLite as the local development database. | Flask database configuration | Implemented |
| SR4 | The system shall use Jinja2 templates for server-side page rendering. | `templates/` | Implemented |
| SR5 | The system shall use Bootstrap and custom CSS to provide a responsive interface. | `templates/base.html`, `static/css/style.css` | Implemented |
| SR6 | The system shall store Guest, Room and Booking records. | `Guest`, `Room` and `Booking` models | Implemented |
| SR7 | The system shall validate required booking fields. | Booking creation workflow | Implemented |
| SR8 | The system shall validate that the check-out date is later than the check-in date. | Backend validation and `static/js/app.js` | Implemented |
| SR9 | The system shall prevent overlapping active bookings for the same room. | Booking overlap validation | Implemented |
| SR10 | The system shall prevent new bookings for rooms under Maintenance. | Booking validation workflow | Implemented |
| SR11 | The system shall update room status during check-in and check-out workflows. | Check-in and check-out workflows | Implemented |
| SR12 | The system shall use vanilla JavaScript for lightweight frontend interaction. | `static/js/app.js` | Implemented |
| SR13 | The system shall include supporting documentation and testing evidence. | `docs/`, `tests/` and `screenshots/` | Implemented |

---

## Functional Requirements

### Guest Management

The system must allow staff to:

- create a guest record;
- view existing guest records;
- store the guest's full name, email address, phone number and notes;
- validate the basic format of the guest email address.

Editing existing guest records remains a planned improvement.

### Room Management

The system must allow staff to:

- view the seeded hotel rooms;
- add a new room;
- view room number, room type, price and status;
- update room status.

Supported room statuses are:

- Available;
- Occupied;
- Cleaning;
- Maintenance.

### Booking Management

The system must allow staff to:

- create a booking;
- view existing bookings;
- cancel a booking;
- check a guest in;
- check a guest out;
- calculate the total price using the room price and number of nights;
- prevent invalid date ranges;
- prevent overlapping active bookings;
- prevent bookings for rooms in Maintenance status.

Supported booking statuses are:

- Pending;
- Confirmed;
- Checked-in;
- Checked-out;
- Cancelled.

### Dashboard

The system must provide a dashboard showing:

- total rooms;
- available rooms;
- occupied rooms;
- cleaning rooms;
- maintenance rooms;
- today's check-ins;
- today's check-outs;
- recent bookings.

### Frontend Interaction

The system should use vanilla JavaScript to improve usability by supporting:

- room status filtering;
- booking status filtering;
- booking date validation before form submission;
- booking cancellation confirmation.

---

## Non-Functional Requirements

| ID | Requirement | Explanation |
|---|---|---|
| NFR1 | Usability | The interface should be simple enough for non-technical hotel staff to understand and operate. |
| NFR2 | Maintainability | The project should use a clear structure with separate models, services, templates, static files and tests. |
| NFR3 | Reliability | The system should reduce double-booking risk through server-side validation. |
| NFR4 | Portability | The application should run locally using Python, Flask and SQLite. |
| NFR5 | Responsiveness | The interface should work reasonably well on common laptop and tablet screen sizes. |
| NFR6 | Data minimisation | The application should store only guest and booking information required for hotel operations. |
| NFR7 | Testability | Important booking, status-transition and notification logic should be capable of automated testing. |
| NFR8 | Security | Credentials and external API configuration must not be hard-coded in source-controlled files. |

---

## Original Unit 36 MVP Scope

The original Unit 36 MVP includes:

- a single staff-facing interface;
- 10 seeded hotel rooms;
- guest creation and viewing;
- room creation and status updates;
- booking creation and viewing;
- check-in and check-out workflows;
- booking cancellation;
- dashboard summaries;
- room and booking filters;
- server-side booking validation;
- basic frontend validation using vanilla JavaScript;
- supporting documentation;
- manual and automated testing evidence.

---

## Unit 37 API Extension

Following completion of the original booking system, the project was extended for Unit 37 with an API-based housekeeping notification workflow.

The implemented extension includes:

| ID | Extension Requirement | Status |
|---|---|---|
| ER1 | Checking out a guest must update the booking and place the room into a cleaning-related operational state. | Implemented |
| ER2 | The system must attempt to send a housekeeping notification through Telegram. | Implemented |
| ER3 | The system must support an email fallback when the primary notification cannot be delivered. | Implemented |
| ER4 | The system must record notification delivery information in a notification log. | Implemented |
| ER5 | Staff must be able to view notification records through the application interface. | Implemented |
| ER6 | The project must support validated staff commands through the Telegram bot workflow. | Implemented |
| ER7 | External API credentials must be loaded through environment variables rather than hard-coded into the application. | Implemented |

The Unit 37 extension is documented separately in:

- `api-integration-overview.md`;
- `api-design-diagrams.md`;
- `notification-workflow-design.md`;
- `email-notification-workflow.md`;
- `telegram-staff-bot-workflow.md`;
- `data-security-report.md`.

---

## Out of Scope

The following features are not included in the current completed application:

- authenticated user accounts;
- role-based access control;
- a customer self-booking portal;
- online payment processing;
- customer-facing email or SMS booking confirmations;
- cloud production deployment;
- a PostgreSQL production database;
- automated database backups;
- a complete system-wide audit trail;
- advanced reporting and revenue analytics;
- assignment of housekeeping tasks to named individual employees.

The implemented notification log records housekeeping notification activity but is not intended to provide a complete system-wide audit trail.

---

## Assumptions

- The hotel initially operates with 10 rooms.
- The application is used internally by hotel staff rather than directly by customers.
- The project is designed primarily for local academic demonstration.
- SQLite is suitable for the prototype and academic assessment stage.
- Staff using the MVP are trusted internal users.
- The application will be evaluated using functional testing, automated tests, screenshots and supporting documentation.

---

## Constraints

- The application is a local prototype rather than a production hotel management platform.
- The MVP does not include authenticated user accounts.
- SQLite has limited suitability for concurrent production use.
- External notifications depend on valid API credentials and internet connectivity.
- The system does not process online payments.
- The system stores only the limited guest information required for the demonstrated workflows.

---

## Success Criteria

The Unit 36 booking and room management system will be considered successful if:

- staff can create guest, room and booking records;
- the system prevents overlapping active bookings;
- bookings cannot be created with invalid date ranges;
- bookings cannot be created for rooms in Maintenance status;
- staff can check guests in and out;
- room status changes correctly during the booking workflow;
- dashboard information supports daily operational decisions;
- validation messages are clear;
- the application is documented and tested;
- the application is presentable for academic submission and portfolio use.

The Unit 37 extension will be considered successful if:

- check-out can trigger the housekeeping notification workflow;
- Telegram notification delivery is attempted;
- email fallback is available when required;
- notification outcomes are recorded;
- staff Telegram commands are validated;
- API credentials remain outside committed source code;
- the original Unit 36 booking functionality continues to operate.