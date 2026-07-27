# Requirement Traceability Matrix

This matrix links the requirements of the Boutique Hotel Booking and Room Management System to design documentation, implementation files, planned tests, recorded results and supporting evidence.

The test identifiers correspond directly to `docs/testing-plan.md` and `docs/test-results-template.md`.

---

## Traceability Status

| Status | Meaning |
|---|---|
| Covered | The requirement is implemented and supported by completed test or implementation evidence |
| Partially Covered | The requirement is implemented, but part of the test result or evidence still requires verification |
| Implementation Evidence | The technical requirement is demonstrated through source-code or configuration evidence and does not require a separate browser test |
| Planned Improvement | The requirement is outside the current MVP and retained for future development |
| Not Covered | The requirement is not implemented |

---

## User Requirement Traceability

| ID | Requirement | Design and Implementation Evidence | Test Result | Evidence | Status |
|---|---|---|---|---|---|
| UR1 | Staff must be able to add and view guest records with contact details. | `models.py`; guest routes in `app.py`; `templates/add_guest.html`; `templates/guests.html` | TC03 Partial; TC04 Pass; TC05 Pass | Guests page, invalid-email and duplicate-email evidence | Partially Covered |
| UR2 | Staff must be able to add rooms and view the hotel room list. | `models.py`; room routes in `app.py`; `templates/add_room.html`; `templates/rooms.html` | TC02 Pass; TC06 Not Run | `screenshots/02-rooms-page.png`; room-creation evidence required | Partially Covered |
| UR3 | Staff must be able to update room status. | Room-status route in `app.py`; `templates/rooms.html` | TC14 Pass | Room-status update evidence | Covered |
| UR4 | Staff must be able to create and manage bookings. | `Booking` model; booking routes in `app.py`; `templates/add_booking.html`; `templates/bookings.html` | TC07 Partial; TC17 Partial | Booking form, booking list and cancellation evidence | Partially Covered |
| UR5 | Staff must be able to check guests in and out. | Check-in and check-out routes in `app.py`; `services/booking_service.py`; `templates/bookings.html` | TC12 Pass; TC13 Pass | Check-in and check-out evidence | Covered |
| UR6 | Staff must be able to view room availability through the dashboard and Rooms page. | Dashboard route; `templates/dashboard.html`; `templates/rooms.html` | TC01 Pass; TC02 Pass; TC18 Partial | `screenshots/01-dashboard.png`; `screenshots/02-rooms-page.png` | Partially Covered |
| UR7 | Managers must be able to view booking activity and room-status summaries. | Dashboard calculations in `app.py`; `templates/dashboard.html` | TC01 Pass; TC18 Partial | Dashboard screenshot; final total comparison required | Partially Covered |
| UR8 | Staff should be able to filter rooms and bookings by status. | `static/js/app.js`; `templates/rooms.html`; `templates/bookings.html` | TC15 Pass; TC16 Pass | `screenshots/04-room-filter.png`; `screenshots/14-booking-filter.png` | Covered |
| UR9 | Staff should receive clear feedback when booking data is invalid. | Booking validation in `app.py`; `services/booking_service.py`; client-side validation in `static/js/app.js` | TC08 Pass; TC09 Pass; TC10 Pass; TC11 Partial | Invalid-date, overlap and Maintenance evidence; additional client-side evidence required | Covered |
| UR10 | Staff should be able to edit guest records when contact details are incorrect. | No Edit Guest route or template in the current MVP | Not tested | No current evidence | Planned Improvement |

---

## System Requirement Traceability

| ID | System Requirement | Implementation Evidence | Related Test or Verification | Status |
|---|---|---|---|---|
| SR1 | The system shall be implemented as a Python Flask web application. | `app.py`; `requirements.txt` | Application starts locally and supports TC01–TC19 | Implementation Evidence |
| SR2 | The system shall use Flask-SQLAlchemy as its ORM. | SQLAlchemy configuration in `app.py`; models in `models.py`; dependency in `requirements.txt` | Source-code verification | Implementation Evidence |
| SR3 | The system shall use SQLite as the local database. | Database configuration in `app.py`; local runtime database | Application and automated-test execution | Implementation Evidence |
| SR4 | The system shall use Jinja2 templates for server-side page rendering. | `templates/`; `render_template` usage in `app.py` | TC01, TC02, TC03, TC07 | Covered |
| SR5 | The system shall use Bootstrap and custom CSS for the staff-facing interface. | `templates/base.html`; `static/css/style.css` | TC19 Partial | Partially Covered |
| SR6 | The system shall store Guest, Room and Booking records. | `Guest`, `Room` and `Booking` models in `models.py` | TC02 Pass; TC03 Partial; TC06 Not Run; TC07 Partial | Partially Covered |
| SR7 | The system shall validate required booking fields and calculate booking totals. | Booking route and service logic in `app.py` and `services/booking_service.py` | TC07 Partial; AT01 Pass | Partially Covered |
| SR8 | The system shall ensure that check-out is later than check-in. | Backend booking validation; client-side validation in `static/js/app.js` | TC08 Pass; TC11 Partial | Covered |
| SR9 | The system shall prevent overlapping active bookings for the same room. | Overlap validation in `services/booking_service.py` and booking route | TC09 Pass; AT01 Pass | Covered |
| SR10 | The system shall prevent bookings for rooms under Maintenance. | Maintenance validation in booking logic | TC10 Pass; AT01 Pass | Covered |
| SR11 | The system shall update booking and room statuses during check-in and check-out. | Check-in and check-out logic in `app.py` and `services/booking_service.py` | TC12 Pass; TC13 Pass; AT01 Pass | Covered |
| SR12 | The system shall use vanilla JavaScript for lightweight frontend interaction. | Filtering, date validation and confirmation logic in `static/js/app.js` | TC11 Partial; TC15 Pass; TC16 Pass; TC17 Partial | Partially Covered |
| SR13 | The system shall validate guest email format and prevent duplicate guest email records. | Guest validation in `app.py`; database constraint or duplicate-checking logic in `models.py` | TC04 Pass; TC05 Pass | Covered |

---

## Non-Functional Requirement Traceability

| ID | Area | Implementation Evidence | Test or Verification | Status |
|---|---|---|---|---|
| NFR1 | Usability | Consistent navigation, forms, tables, labels and staff-facing page structure | TC19 Partial | Partially Covered |
| NFR2 | Maintainability | Separation of models, templates, static assets, services, tests and documentation | Source-code and project-structure verification | Implementation Evidence |
| NFR3 | Reliability | Validation, controlled status transitions and automated regression testing | AT01 Pass; TC08–TC13 | Covered |
| NFR4 | Portability | Local dependency installation, SQLite and documented run command | Local macOS execution; `requirements.txt`; `README.md` | Implementation Evidence |
| NFR5 | Responsiveness | Bootstrap layout and responsive frontend structure | TC19 Partial | Partially Covered |
| NFR6 | Data minimisation | Core booking records store only information required for hotel operations | Model and form review | Implementation Evidence |
| NFR7 | Testability | Reusable service logic, pytest tests and documented test cases | AT01–AT03; `tests/`; testing documentation | Covered |
| NFR8 | Security | Server-side validation, environment-variable handling for later integrations and no hard-coded production credentials | Source-code and configuration review | Implementation Evidence |

---

## Automated Test Traceability

| Test ID | Test Area | Implementation Evidence | Recorded Result | Status |
|---|---|---|---|---|
| AT01 | Complete regression suite | All files in `tests/` | Latest recorded result: `34 passed` | Pass |
| AT02 | Booking-service rules | `tests/test_booking_service.py` | Included in successful complete test run | Pass |
| AT03 | Notification-extension regression | `tests/test_checkout_notifications.py`; `tests/test_notification_service.py`; `tests/test_telegram_command_service.py` | Included in successful complete test run | Pass |

The final pytest result must be updated if the test count or outcome changes before submission.

---

## Development Evidence

The following evidence supports the development process but is not treated as functional test execution:

| Evidence Area | Relevant Evidence |
|---|---|
| Project organisation | VS Code project-structure screenshot |
| Backend implementation | `app.py`, `models.py`, `services/` |
| Frontend implementation | `templates/`, `static/css/style.css`, `static/js/app.js` |
| Version control | Git status, branches and commit history |
| Pull-request workflow | GitHub pull-request and changed-files screenshots |
| Documentation | `docs/`, `README.md` and report appendices |

These items should remain in `docs/development-log.md` or the main report appendix rather than being assigned manual functional-test IDs.

---

## Outstanding Traceability Items

| Related Test or Requirement | Required Action |
|---|---|
| TC03 / UR1 | Capture or verify a successfully created guest appearing in the Guests list |
| TC06 / UR2 | Complete the new-room creation test and record the resulting room |
| TC07 / UR4 / SR7 | Link a controlled booking submission to its calculated total price |
| TC11 / SR12 | Capture client-side validation before the form is submitted |
| TC17 / UR4 / SR12 | Record both cancellation-confirmation outcomes |
| TC18 / UR6 / UR7 | Compare dashboard totals directly with current records |
| TC19 / NFR1 / NFR5 | Record reduced-width usability and responsiveness |
| AT01 | Run `pytest -q` once more and retain the final terminal output |
| UR10 | Retain guest editing as a future improvement |

---

## Conclusion

The matrix demonstrates traceability from the project requirements to design, implementation, testing and evidence.

The core room, booking, validation, filtering, check-in and check-out requirements are implemented. Some requirements remain partially covered because their final test evidence still needs to be completed or verified.

Guest editing remains outside the current MVP. Authentication, role-based access, production deployment and advanced reporting are also retained as future improvements rather than current implementation requirements.