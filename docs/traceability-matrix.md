

# Requirement Traceability Matrix

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This traceability matrix links the original user and system requirements to the implemented application features, supporting files, testing evidence and current completion status.

It supports the Unit 36 development portfolio by demonstrating that the application was developed against defined requirements rather than built without a clear plan.

---

## Traceability Status Key

| Status | Meaning |
|---|---|
| Implemented | Requirement is covered by the current MVP |
| Partially Implemented | Requirement is partly covered but needs further improvement |
| In Progress | Requirement is currently being documented or tested |
| Planned Improvement | Requirement is outside the current MVP but suitable for future development |
| Not Implemented | Requirement is not currently covered |

---

## User Requirement Traceability

| Requirement ID | User Requirement | Implemented Feature | Main File(s) | Testing Evidence | Status |
|---|---|---|---|---|---|
| UR1 | Staff must be able to add and view guest records with contact details. | Add Guest form and Guests list | `app.py`, `templates/add_guest.html`, `templates/guests.html`, `models.py` | T03, T04; screenshots `03-add-guest.png`, `04-invalid-email.png` | Implemented |
| UR2 | Staff must be able to add rooms and view the list of hotel rooms. | Add Room form, seeded rooms and Rooms list | `app.py`, `templates/add_room.html`, `templates/rooms.html`, `models.py` | T02, T05; screenshots `02-rooms-list.png`, `05-add-room.png` | Implemented |
| UR3 | Staff must be able to update room status. | Room status update form on Rooms page | `app.py`, `templates/rooms.html` | T03 / TC13; screenshot `13-room-status-update.png` | Implemented |
| UR4 | Staff must be able to create and manage bookings. | Add Booking form, Bookings list and cancellation action | `app.py`, `templates/add_booking.html`, `templates/bookings.html`, `models.py` | T06, T14 / TC06, TC18; screenshots `06-create-booking.png`, `18-cancel-confirmation.png` | Implemented |
| UR5 | Staff must be able to check guests in and out. | Check-in and check-out actions | `app.py`, `templates/bookings.html` | T10, T11 / TC11, TC12; screenshots `11-check-in.png`, `12-check-out.png` | Implemented |
| UR6 | Staff must be able to see room availability from a dashboard and rooms page. | Dashboard summary cards and Rooms table | `app.py`, `templates/dashboard.html`, `templates/rooms.html` | T01, T02, T19; screenshots `01-dashboard.png`, `02-rooms-list.png`, `19-dashboard-counts.png` | Implemented |
| UR7 | Managers must be able to view booking activity and room status summaries. | Dashboard overview and recent bookings section | `app.py`, `templates/dashboard.html` | T01, T19; screenshots `01-dashboard.png`, `19-dashboard-counts.png` | Implemented |
| UR8 | Staff should be able to filter rooms and bookings by status. | Vanilla JavaScript room and booking filters | `static/js/app.js`, `templates/rooms.html`, `templates/bookings.html` | T12, T13 / TC14, TC16; screenshots `14-room-filter.png`, `16-booking-filter.png` | Implemented / being refined |
| UR9 | Staff should receive clear validation feedback when booking data is invalid. | Backend validation and frontend date validation | `app.py`, `static/js/app.js`, `templates/add_booking.html` | T07, T08, T09, T10; screenshots `07-invalid-date.png`, `08-overlap-validation.png`, `09-maintenance-validation.png`, `10-client-date-validation.png` | Implemented |
| UR10 | Staff should be able to edit guest records if contact details are entered incorrectly. | Edit Guest workflow | Planned: `app.py`, `templates/edit_guest.html`, `templates/guests.html` | Planned future test | Planned Improvement |

---

## System Requirement Traceability

| Requirement ID | System Requirement | Implementation Evidence | Related Test(s) | Status |
|---|---|---|---|---|
| SR1 | The system shall be implemented as a Python Flask web application. | `app.py`, `requirements.txt` | TC01 | Implemented |
| SR2 | The system shall use Flask-SQLAlchemy as the ORM. | `models.py`, `requirements.txt` | TC02, TC03, TC06 | Implemented |
| SR3 | The system shall use SQLite as the local development database. | SQLite configuration in `app.py`; runtime database in `instance/` | TC02, TC03, TC06 | Implemented |
| SR4 | The system shall use Jinja2 templates for server-side rendering. | `templates/` folder | TC01, TC02, TC03, TC06 | Implemented |
| SR5 | The system shall use Bootstrap and custom CSS for a responsive interface. | `templates/base.html`, `static/css/style.css` | TC20 | Implemented / being refined |
| SR6 | The system shall store Guest, Room and Booking records. | `Guest`, `Room`, `Booking` models in `models.py` | TC02, TC03, TC06 | Implemented |
| SR7 | The system shall validate required booking fields. | Booking route validation in `app.py` | TC06, TC07 | Implemented |
| SR8 | The system shall validate that check-out date is after check-in date. | Backend validation in `app.py`; frontend validation in `static/js/app.js` | TC07, TC10 | Implemented |
| SR9 | The system shall prevent overlapping active bookings for the same room. | Overlap query in booking creation route | TC08 | Implemented |
| SR10 | The system shall prevent bookings for rooms under Maintenance. | Maintenance-room validation in booking route | TC09 | Implemented |
| SR11 | The system shall update room status after check-in and check-out. | Check-in/check-out routes in `app.py` | TC11, TC12 | Implemented |
| SR12 | The system shall use vanilla JavaScript for lightweight frontend interaction. | `static/js/app.js` | TC10, TC14, TC16, TC18 | Implemented |
| SR13 | The system shall include documentation and testing evidence. | `docs/` folder and planned `screenshots/` evidence | TC01-TC20 | In Progress |

---

## Feature-to-Evidence Matrix

| Feature | User Value | Code Evidence | Documentation Evidence | Screenshot Evidence |
|---|---|---|---|---|
| Dashboard | Gives staff and managers a quick operational overview | `templates/dashboard.html`, dashboard route in `app.py` | `docs/user-guide.md`, `docs/testing-plan.md` | `01-dashboard.png`, `19-dashboard-counts.png` |
| Room list | Shows current room availability and status | `templates/rooms.html`, `Room` model | `docs/user-guide.md`, `docs/requirements.md` | `02-rooms-list.png` |
| Room status update | Helps reception and housekeeping coordinate room readiness | room status route in `app.py`, `templates/rooms.html` | `docs/user-guide.md`, `docs/testing-plan.md` | `13-room-status-update.png` |
| Guest creation | Allows staff to store guest contact details | add guest route in `app.py`, `Guest` model | `docs/user-guide.md`, `docs/requirements.md` | `03-add-guest.png` |
| Guest email validation | Reduces incorrect guest data entry | add guest route in `app.py` | `docs/testing-plan.md` | `04-invalid-email.png` |
| Booking creation | Allows staff to reserve rooms for guests | add booking route in `app.py`, `Booking` model | `docs/user-guide.md`, `docs/testing-plan.md` | `06-create-booking.png` |
| Invalid date validation | Prevents impossible bookings | `app.py`, `static/js/app.js` | `docs/testing-plan.md` | `07-invalid-date.png`, `10-client-date-validation.png` |
| Overlap prevention | Reduces double-booking risk | overlap validation query in `app.py` | `docs/requirements.md`, `docs/testing-plan.md` | `08-overlap-validation.png` |
| Maintenance-room prevention | Prevents unusable rooms being booked | maintenance validation in `app.py` | `docs/requirements.md`, `docs/testing-plan.md` | `09-maintenance-validation.png` |
| Check-in workflow | Updates booking and room status when guest arrives | check-in route in `app.py` | `docs/user-guide.md` | `11-check-in.png` |
| Check-out workflow | Updates room to Cleaning after guest leaves | check-out route in `app.py` | `docs/user-guide.md` | `12-check-out.png` |
| Room filtering | Helps staff find rooms by status quickly | `static/js/app.js`, `templates/rooms.html` | `docs/testing-plan.md` | `14-room-filter.png`, `15-room-empty-filter.png` |
| Booking filtering | Helps staff find bookings by status quickly | `static/js/app.js`, `templates/bookings.html` | `docs/testing-plan.md` | `16-booking-filter.png`, `17-booking-empty-filter.png` |
| Cancel confirmation | Reduces accidental booking cancellation | `static/js/app.js`, `templates/bookings.html` | `docs/testing-plan.md` | `18-cancel-confirmation.png` |

---

## Coverage Summary

| Category | Coverage Summary |
|---|---|
| Core business workflows | Guest creation, room management, booking creation, check-in and check-out are implemented. |
| Validation | Invalid dates, overlapping bookings and maintenance-room booking prevention are implemented. |
| Frontend interaction | Room and booking filters, date validation and cancel confirmation are implemented using vanilla JavaScript. |
| Documentation | Requirements, testing plan, test results template, technical notes, development log and peer review are documented or in progress. |
| Testing evidence | Test plan and screenshot names are prepared; final screenshots still need to be captured. |
| Future improvements | Guest editing, authentication, deployment and advanced reporting are planned improvements. |

---

## Requirements Not Fully Covered

| Requirement | Reason | Planned Action |
|---|---|---|
| UR10: Edit guest records | The current MVP supports adding and viewing guests but not editing them. | Add an Edit Guest route, template and button in a future branch. |
| SR13: Documentation and testing evidence | Documentation is being prepared, but final screenshots and actual results still need to be completed. | Complete manual testing, capture screenshots and update the test results table. |
| Portfolio-level UI quality | The current interface is functional but still needs final visual polish. | Improve `base.html`, dashboard, forms, tables and `style.css` in a UI polish branch. |

---

## Traceability Conclusion

The traceability matrix shows that the MVP covers the main operational requirements for the boutique hotel scenario. The strongest areas are booking validation, room status management and check-in/check-out workflows.

The main remaining improvements are guest editing, final screenshot evidence and visual polish. These are realistic future enhancements and do not prevent the current MVP from meeting the core academic and business objectives.