# Requirement Traceability Matrix

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This traceability matrix links the user requirements, system requirements, implemented features, source files, manual test cases and screenshot evidence for the Boutique Hotel Booking and Room Management System.

It demonstrates that the application was built against defined requirements and that the final implementation was manually tested using documented evidence.

---

## Traceability Status Key

| Status | Meaning |
|---|---|
| Covered | Requirement is implemented and tested in the current MVP |
| Partially Covered | Requirement is partly implemented but needs further improvement |
| Planned Improvement | Requirement is outside the current MVP and suitable for future development |
| Not Covered | Requirement is not currently implemented |

---

## User Requirement Traceability

| Requirement ID | User Requirement | Implemented Feature | Main File(s) | Test Case(s) | Screenshot Evidence | Status |
|---|---|---|---|---|---|---|
| UR1 | Staff must be able to add and view guest records with contact details. | Add Guest form, Guests table, email validation and duplicate email prevention. | `app.py`, `models.py`, `templates/add_guest.html`, `templates/guests.html` | T05, T06, T07, T08 | `screenshots/05-guests-page.png`, `screenshots/06-add-guest-form.png`, `screenshots/07-invalid-email-validation.png`, `screenshots/08-duplicate-email-validation.png` | Covered |
| UR2 | Staff must be able to add rooms and view the list of hotel rooms. | Add Room form, seeded room records and Rooms table. | `app.py`, `models.py`, `templates/add_room.html`, `templates/rooms.html` | T02 | `screenshots/02-rooms-page.png` | Covered |
| UR3 | Staff must be able to update room status. | Room status update form on the Rooms page. | `app.py`, `templates/rooms.html` | T03 | `screenshots/03-room-status-update.png` | Covered |
| UR4 | Staff must be able to create and manage bookings. | Add Booking form, Bookings table, cancellation action and booking workflow controls. | `app.py`, `models.py`, `templates/add_booking.html`, `templates/bookings.html` | T09, T13, T17 | `screenshots/09-add-booking-form.png`, `screenshots/13-bookings-page.png`, `screenshots/17-cancel-confirmation.png` | Covered |
| UR5 | Staff must be able to check guests in and out. | Check-in and check-out actions that update booking and room status. | `app.py`, `templates/bookings.html` | T15, T16 | `screenshots/15-check-in-result.png`, `screenshots/16-check-out-result.png` | Covered |
| UR6 | Staff must be able to see room availability from a dashboard and rooms page. | Dashboard summary cards and Rooms page status information. | `app.py`, `templates/dashboard.html`, `templates/rooms.html` | T01, T02 | `screenshots/01-dashboard.png`, `screenshots/02-rooms-page.png` | Covered |
| UR7 | Managers must be able to view booking activity and room status summaries. | Dashboard overview, room counts, today's check-ins, today's check-outs and recent booking activity. | `app.py`, `templates/dashboard.html` | T01 | `screenshots/01-dashboard.png` | Covered |
| UR8 | Staff should be able to filter rooms and bookings by status. | Vanilla JavaScript room filter and booking filter. | `static/js/app.js`, `templates/rooms.html`, `templates/bookings.html` | T04, T14 | `screenshots/04-room-filter.png`, `screenshots/14-booking-filter.png` | Covered |
| UR9 | Staff should receive clear validation feedback when booking data is invalid. | Backend booking validation, frontend date validation, overlap prevention and maintenance-room booking prevention. | `app.py`, `static/js/app.js`, `templates/add_booking.html` | T10, T11, T12 | `screenshots/10-invalid-booking-date.png`, `screenshots/11-maintenance-room-booking-prevention.png`, `screenshots/12-overlap-booking-prevention.png` | Covered |
| UR10 | Staff should be able to edit guest records if contact details are entered incorrectly. | Edit Guest workflow. | Planned future files: `templates/edit_guest.html`, updated `app.py` and `templates/guests.html` | Not tested in current MVP | No current screenshot evidence | Planned Improvement |

---

## System Requirement Traceability

| Requirement ID | System Requirement | Implementation Evidence | Related Test Case(s) | Screenshot Evidence | Status |
|---|---|---|---|---|---|
| SR1 | The system shall be implemented as a Python Flask web application. | `app.py`, `requirements.txt` | T19 | `screenshots/19-vscode-app-routes.png` | Covered |
| SR2 | The system shall use Flask-SQLAlchemy as the ORM. | `models.py`, `requirements.txt` | T20 | `screenshots/20-vscode-models.png` | Covered |
| SR3 | The system shall use SQLite as the local development database. | SQLite configuration in `app.py`; local runtime database stored in `instance/`. | T20 | `screenshots/20-vscode-models.png` | Covered |
| SR4 | The system shall use Jinja2 templates for server-side rendering. | `templates/` folder and `render_template` usage in `app.py`. | T18, T19 | `screenshots/18-vscode-project-structure.png`, `screenshots/19-vscode-app-routes.png` | Covered |
| SR5 | The system shall use Bootstrap and custom CSS for a responsive interface. | `templates/base.html`, `static/css/style.css` | T21 | `screenshots/21-vscode-frontend-files.png` | Covered |
| SR6 | The system shall store Guest, Room and Booking records. | `Guest`, `Room` and `Booking` models in `models.py`. | T05, T13, T20 | `screenshots/05-guests-page.png`, `screenshots/13-bookings-page.png`, `screenshots/20-vscode-models.png` | Covered |
| SR7 | The system shall validate required booking fields. | Booking creation route validation in `app.py`. | T09, T10 | `screenshots/09-add-booking-form.png`, `screenshots/10-invalid-booking-date.png` | Covered |
| SR8 | The system shall validate that check-out date is after check-in date. | Backend validation in `app.py` and frontend validation in `static/js/app.js`. | T10 | `screenshots/10-invalid-booking-date.png` | Covered |
| SR9 | The system shall prevent overlapping active bookings for the same room. | Overlap query in booking creation route. | T12 | `screenshots/12-overlap-booking-prevention.png` | Covered |
| SR10 | The system shall prevent bookings for rooms under Maintenance. | Maintenance-room validation in booking creation route. | T11 | `screenshots/11-maintenance-room-booking-prevention.png` | Covered |
| SR11 | The system shall update room status after check-in and check-out. | Check-in and check-out routes in `app.py`. | T15, T16 | `screenshots/15-check-in-result.png`, `screenshots/16-check-out-result.png` | Covered |
| SR12 | The system shall use vanilla JavaScript for lightweight frontend interaction. | `static/js/app.js` for filtering, date validation and cancel confirmation. | T04, T14, T17, T21 | `screenshots/04-room-filter.png`, `screenshots/14-booking-filter.png`, `screenshots/17-cancel-confirmation.png`, `screenshots/21-vscode-frontend-files.png` | Covered |
| SR13 | The system shall include documentation and testing evidence. | `docs/` folder, testing document, traceability matrix, screenshots and GitHub evidence. | T18, T22, T23, T24, T25 | `screenshots/18-vscode-project-structure.png`, `screenshots/22-terminal-git-clean.png`, `screenshots/23-github-pull-request.png`, `screenshots/24-github-files-changed.png`, `screenshots/25-github-branch.png` | Covered |

---

## Feature-to-Evidence Matrix

| Feature | User Value | Code Evidence | Documentation Evidence | Test Case(s) | Screenshot Evidence |
|---|---|---|---|---|---|
| Dashboard | Gives staff and managers a quick operational overview. | `templates/dashboard.html`, dashboard route in `app.py` | `docs/user-guide.md`, `docs/testing-plan.md`, `docs/test-results-template.md` | T01 | `screenshots/01-dashboard.png` |
| Room list | Shows current room availability and room readiness. | `templates/rooms.html`, `Room` model in `models.py` | `docs/user-guide.md`, `docs/requirements.md` | T02 | `screenshots/02-rooms-page.png` |
| Room status update | Helps reception and housekeeping coordinate room readiness. | room status update route in `app.py`, `templates/rooms.html` | `docs/user-guide.md`, `docs/testing-plan.md` | T03 | `screenshots/03-room-status-update.png` |
| Room filtering | Helps staff find rooms by status quickly. | `static/js/app.js`, `templates/rooms.html` | `docs/testing-plan.md`, `docs/test-results-template.md` | T04 | `screenshots/04-room-filter.png` |
| Guest list | Allows staff to review guest contact records. | `templates/guests.html`, `Guest` model in `models.py` | `docs/user-guide.md`, `docs/requirements.md` | T05 | `screenshots/05-guests-page.png` |
| Guest creation | Allows staff to store guest contact details. | add guest route in `app.py`, `templates/add_guest.html` | `docs/user-guide.md`, `docs/requirements.md` | T06 | `screenshots/06-add-guest-form.png` |
| Guest email validation | Reduces incorrect guest data entry. | email validation in `app.py` | `docs/testing-plan.md`, `docs/test-results-template.md` | T07, T08 | `screenshots/07-invalid-email-validation.png`, `screenshots/08-duplicate-email-validation.png` |
| Booking creation | Allows staff to reserve rooms for guests. | add booking route in `app.py`, `Booking` model in `models.py`, `templates/add_booking.html` | `docs/user-guide.md`, `docs/testing-plan.md` | T09 | `screenshots/09-add-booking-form.png` |
| Invalid date validation | Prevents impossible bookings. | `app.py`, `static/js/app.js` | `docs/testing-plan.md`, `docs/test-results-template.md` | T10 | `screenshots/10-invalid-booking-date.png` |
| Maintenance-room prevention | Prevents unusable rooms being booked. | maintenance validation in `app.py` | `docs/requirements.md`, `docs/testing-plan.md` | T11 | `screenshots/11-maintenance-room-booking-prevention.png` |
| Overlap prevention | Reduces double-booking risk. | overlap validation query in `app.py` | `docs/requirements.md`, `docs/testing-plan.md` | T12 | `screenshots/12-overlap-booking-prevention.png` |
| Bookings list | Shows booking status, dates, room, guest, price and actions. | `templates/bookings.html`, bookings route in `app.py` | `docs/user-guide.md`, `docs/testing-plan.md` | T13 | `screenshots/13-bookings-page.png` |
| Booking filtering | Helps staff find bookings by status quickly. | `static/js/app.js`, `templates/bookings.html` | `docs/testing-plan.md`, `docs/test-results-template.md` | T14 | `screenshots/14-booking-filter.png` |
| Check-in workflow | Updates booking and room status when the guest arrives. | check-in route in `app.py`, `templates/bookings.html` | `docs/user-guide.md` | T15 | `screenshots/15-check-in-result.png` |
| Check-out workflow | Updates room to Cleaning after the guest leaves. | check-out route in `app.py`, `templates/bookings.html` | `docs/user-guide.md` | T16 | `screenshots/16-check-out-result.png` |
| Cancel confirmation | Reduces accidental booking cancellation. | `static/js/app.js`, `templates/bookings.html` | `docs/testing-plan.md`, `docs/test-results-template.md` | T17 | `screenshots/17-cancel-confirmation.png` |
| Project structure | Demonstrates maintainable organisation of source code and evidence. | `app.py`, `models.py`, `templates/`, `static/`, `docs/`, `screenshots/` | `README.md`, `docs/technical-notes.md` | T18 | `screenshots/18-vscode-project-structure.png` |
| Version control | Demonstrates use of GitHub workflow and pull request review. | Git branch, commits and pull request | `README.md`, `docs/development-log.md` | T22, T23, T24, T25 | `screenshots/22-terminal-git-clean.png`, `screenshots/23-github-pull-request.png`, `screenshots/24-github-files-changed.png`, `screenshots/25-github-branch.png` |

---

## Coverage Summary

| Category | Coverage Summary |
|---|---|
| Core business workflows | Guest creation, room management, booking creation, cancellation, check-in and check-out are implemented and tested. |
| Validation | Invalid dates, duplicate email addresses, overlapping bookings and maintenance-room booking prevention are implemented and tested. |
| Frontend interaction | Room filtering, booking filtering, date validation and cancel confirmation are implemented using vanilla JavaScript. |
| Documentation | Requirements, testing plan, manual test results, technical notes, development log, user guide, peer review and traceability matrix are documented. |
| Testing evidence | Manual test results are linked to 25 screenshot references covering application functionality, development evidence and GitHub workflow evidence. |
| Version control | GitHub pull request workflow, commit history and branch evidence are documented through screenshots. |
| Future improvements | Guest editing, authentication, deployment, email confirmations and advanced reporting remain planned improvements. |

---

## Requirements Not Fully Covered

| Requirement | Reason | Planned Action |
|---|---|---|
| UR10: Edit guest records | The current MVP supports adding and viewing guests but does not yet include a guest editing workflow. | Add an Edit Guest route, template and action button in a future branch. |
| Authentication and role-based access | The current MVP is designed as a local staff-facing prototype without login roles. | Add receptionist, housekeeping and manager roles in a future release. |
| Cloud deployment | The current version runs locally using Flask and SQLite. | Deploy to a cloud platform and use PostgreSQL for production-style hosting. |
| Email or SMS confirmations | The current MVP does not integrate external communication APIs. | Add email or messaging API integration in a future extension. |
| Advanced reporting | The dashboard provides operational summary data but not historical analytics charts. | Add occupancy and revenue reporting charts in a future iteration. |

---

## Traceability Conclusion

The traceability matrix shows that the current MVP covers the main operational requirements for the boutique hotel scenario. The strongest areas are room management, booking validation, check-in/check-out workflows, frontend filtering and documented testing evidence.

The implemented system provides a working staff-facing application supported by manual test results, screenshot evidence, documentation and GitHub workflow evidence. The remaining gaps are realistic future improvements rather than blockers for the current MVP.