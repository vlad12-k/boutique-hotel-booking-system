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

# Requirements Specification

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This document defines the user requirements, system requirements and MVP scope for the hotel booking and room management application. It supports the Unit 36 design and development evidence by showing what the application is expected to achieve and how the implemented features relate to the original business problem.

---

## Business Context

The client is a small boutique hotel with 10 rooms. The hotel requires a simple internal web application to help staff manage guests, rooms and bookings more reliably than a paper-based or spreadsheet-based process.

The main operational problem is that manual booking and room tracking can lead to:

- double bookings;
- unclear room availability;
- delayed room status updates;
- poor coordination between reception and housekeeping;
- limited visibility for managers.

The proposed system is a staff-facing web application that allows reception staff and managers to manage daily hotel operations from one place.

---

## User Roles

| User Role | Description | Main Needs |
|---|---|---|
| Reception Staff | Staff responsible for guests, bookings, check-ins and check-outs | Create guest records, create bookings, check guests in and out, view availability |
| Housekeeping Staff | Staff responsible for room readiness | View and update room status such as Cleaning, Maintenance and Available |
| Hotel Manager | Person responsible for operational oversight | View dashboard summary, monitor bookings and room activity |

The MVP uses a single staff-facing interface and does not include role-based authentication. Role separation is identified as a future improvement.

---

## User Requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| UR1 | Staff must be able to add and view guest records with contact details. | High | Implemented |
| UR2 | Staff must be able to add rooms and view the list of hotel rooms. | High | Implemented |
| UR3 | Staff must be able to update room status. | High | Implemented |
| UR4 | Staff must be able to create and manage bookings. | High | Implemented |
| UR5 | Staff must be able to check guests in and out. | High | Implemented |
| UR6 | Staff must be able to see room availability from a dashboard and rooms page. | High | Implemented |
| UR7 | Managers must be able to view booking activity and room status summaries. | Medium | Implemented |
| UR8 | Staff should be able to filter rooms and bookings by status. | Medium | Implemented |
| UR9 | Staff should receive clear validation feedback when booking data is invalid. | High | Implemented |
| UR10 | Staff should be able to edit guest records if contact details are entered incorrectly. | Medium | Planned improvement |

---

## System Requirements

| ID | Requirement | Implementation Evidence | Status |
|---|---|---|---|
| SR1 | The system shall be implemented as a Python Flask web application. | `app.py` | Implemented |
| SR2 | The system shall use Flask-SQLAlchemy as the ORM. | `models.py` | Implemented |
| SR3 | The system shall use SQLite as the local development database. | Flask configuration in `app.py` | Implemented |
| SR4 | The system shall use Jinja2 templates for server-side rendering. | `templates/` folder | Implemented |
| SR5 | The system shall use Bootstrap and custom CSS for a responsive interface. | `templates/base.html`, `static/css/style.css` | Implemented |
| SR6 | The system shall store Guest, Room and Booking records. | `Guest`, `Room`, `Booking` models | Implemented |
| SR7 | The system shall validate required booking fields. | Booking route validation | Implemented |
| SR8 | The system shall validate that check-out date is after check-in date. | Backend validation and `static/js/app.js` | Implemented |
| SR9 | The system shall prevent overlapping active bookings for the same room. | Booking overlap query in `app.py` | Implemented |
| SR10 | The system shall prevent bookings for rooms under Maintenance. | Booking validation in `app.py` | Implemented |
| SR11 | The system shall update room status after check-in and check-out. | Check-in/check-out routes | Implemented |
| SR12 | The system shall use vanilla JavaScript for lightweight frontend interaction. | `static/js/app.js` | Implemented |
| SR13 | The system shall include documentation and testing evidence. | `docs/` folder | In progress |

---

## Functional Requirements

### Guest Management

The system must allow staff to:

- create a guest record;
- view existing guest records;
- store guest full name, email address, phone number and notes;
- validate basic guest email format.

Planned improvement:

- edit existing guest records.

### Room Management

The system must allow staff to:

- view seeded rooms;
- add a new room;
- view room number, type, price and status;
- update room status.

Supported room statuses:

- Available;
- Occupied;
- Cleaning;
- Maintenance.

### Booking Management

The system must allow staff to:

- create a booking;
- view bookings;
- cancel bookings;
- check guests in;
- check guests out;
- calculate total price based on room price and number of nights;
- prevent invalid date ranges;
- prevent overlapping active bookings;
- prevent bookings for rooms in Maintenance status.

Supported booking statuses:

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
- cancellation confirmation.

---

## Non-Functional Requirements

| ID | Requirement | Explanation |
|---|---|---|
| NFR1 | Usability | The interface should be simple enough for non-technical hotel staff. |
| NFR2 | Maintainability | The code should use a clear Flask project structure with separate templates, static files and models. |
| NFR3 | Reliability | The system should reduce double-booking risk through backend validation. |
| NFR4 | Portability | The application should run locally using Python, Flask and SQLite. |
| NFR5 | Responsiveness | The interface should work reasonably well on common laptop and tablet screen sizes. |
| NFR6 | Data minimisation | The MVP should only store operationally necessary guest and booking data. |

---

## MVP Scope

The MVP includes:

- single staff-facing interface;
- 10 seeded hotel rooms;
- guest creation and viewing;
- room creation and status updates;
- booking creation and viewing;
- check-in and check-out workflow;
- booking cancellation;
- dashboard summary;
- room and booking filters;
- server-side booking validation;
- basic frontend validation using vanilla JavaScript;
- support documentation and testing templates.

---

## Out of Scope for MVP

The following features are not included in the MVP but are suitable for future development:

- role-based authentication;
- customer self-booking portal;
- online payments;
- email or SMS booking confirmations;
- cloud deployment;
- PostgreSQL production database;
- automated backups;
- audit logs;
- advanced reporting and revenue analytics;
- housekeeping task assignment.

---

## Assumptions

- The hotel has 10 rooms.
- The system is used internally by staff, not directly by customers.
- The MVP is designed for local academic demonstration rather than production deployment.
- SQLite is acceptable for the prototype stage.
- The application will be evaluated through manual testing, screenshots and documentation evidence.

---

## Success Criteria

The project will be considered successful if:

- staff can create guests, rooms and bookings;
- the system prevents overlapping active bookings;
- staff can check guests in and out;
- room status changes correctly during the booking workflow;
- dashboard information supports daily operational decisions;
- validation messages are clear;
- the system is documented and tested against the requirements;
- the final application is presentable for academic submission and portfolio use.