# Testing Plan

This document defines the testing approach for the Boutique Hotel Booking and Room Management System.

It identifies the main workflows, validation rules, expected outcomes and evidence required. Actual outcomes, Pass/Fail decisions and defects are recorded separately in `docs/test-results-template.md`.

---

## Testing Scope

Testing covers the core Application Development functionality:

- dashboard and navigation;
- guest management;
- room management;
- booking creation and price calculation;
- booking-date validation;
- duplicate-guest validation;
- overlapping-booking prevention;
- Maintenance-room restrictions;
- check-in and check-out;
- room and booking status changes;
- room and booking filtering;
- booking-cancellation confirmation;
- basic usability and responsiveness.

The following areas are outside the current MVP scope:

- authenticated user accounts;
- role-based access control;
- customer self-booking;
- online payments;
- production cloud deployment;
- large-scale performance testing;
- penetration testing.

Testing combines:

- manual functional testing of pages, forms and workflows;
- negative testing of invalid or restricted actions;
- automated pytest testing of reusable business logic;
- regression testing after changes to booking or room-status behaviour.

The complete pytest suite also includes tests for the later housekeeping notification extension. Detailed API-specific evidence is documented separately.

---

## Test Environment

| Item | Details |
|---|---|
| Backend | Python Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Frontend | Jinja2, Bootstrap, custom CSS and vanilla JavaScript |
| Operating system | macOS |
| Tester | Vladyslav Kononov |
| Local URL | `http://127.0.0.1:5000` |
| Application command | `python app.py` |
| Browser | Browser name and version to be recorded during test execution |

---

## Test Priority

| Priority | Meaning |
|---|---|
| High | Core workflow, validation rule or data-integrity protection |
| Medium | Important usability or frontend behaviour |

---

## Planned Manual Tests

The test identifiers and requirement links must remain consistent with `docs/requirements.md`, `docs/test-results-template.md` and `docs/traceability-matrix.md`.

| Test ID | Priority | Requirement or Risk | Input or Action | Expected Result | Planned Evidence |
|---|---|---|---|---|---|
| TC01 | High | UR6, UR7 | Start the application and open `/`. | The dashboard displays room counts, booking information and recent bookings without an application error. | Dashboard screenshot |
| TC02 | High | UR2, UR6, SR6 | Open `/rooms`. | The original seeded rooms are displayed with room number, type, price and status. | Rooms-page screenshot |
| TC03 | High | UR1, SR6 | Enter valid details in the Add Guest form and submit. | A new guest is created and displayed on the Guests page. | Add Guest form and resulting guest record |
| TC04 | High | UR1, SR13 | Submit an invalid email address in the Add Guest form. | A validation message is displayed and the guest is not created. | Validation-message screenshot |
| TC05 | High | UR1, SR13 | Attempt to create another guest using an existing email address. | The duplicate guest record is rejected and an appropriate message is displayed. | Duplicate-validation screenshot |
| TC06 | High | UR2, SR6 | Enter a unique room number and valid details in the Add Room form. | A new room is created and displayed on the Rooms page. | Add Room form and resulting room record |
| TC07 | High | UR4, SR7, SR8 | Create a booking using a valid guest, room and date range. | The booking is created and displays the correct total price. | Booking form and resulting booking record |
| TC08 | High | UR9, SR8 | Submit a booking where check-out is equal to or earlier than check-in. | The booking is rejected and a validation message is displayed. | Invalid-date validation screenshot |
| TC09 | High | UR9, SR9 | Attempt to create an overlapping active booking for the same room. | The second booking is rejected and an overlap warning is displayed. | Overlap-validation screenshot |
| TC10 | High | UR9, SR10 | Set a room to Maintenance and attempt to book it. | The booking is rejected and a Maintenance warning is displayed. | Maintenance-validation screenshot |
| TC11 | Medium | SR8, SR12 | Submit the booking form with missing dates or an invalid date order. | Client-side validation blocks submission and displays an inline message. | Client-side validation screenshot |
| TC12 | High | UR5, SR11 | Check in an eligible Pending or Confirmed booking. | The booking status becomes Checked-in and the room status becomes Occupied. | Before-and-after booking and room evidence |
| TC13 | High | UR5, SR11 | Check out a Checked-in booking. | The booking status becomes Checked-out and the room status becomes Cleaning. | Before-and-after booking and room evidence |
| TC14 | High | UR3, SR11 | Change a room from Cleaning to Available. | The new room status is saved and displayed correctly. | Room-status screenshot |
| TC15 | Medium | UR8, SR12 | Apply each room-status filter and then select All. | Only matching rooms are displayed, and All restores the complete list without reloading the page. | Room-filter screenshot |
| TC16 | Medium | UR8, SR12 | Apply each booking-status filter and then select All. | Only matching bookings are displayed, and All restores the complete list without reloading the page. | Booking-filter screenshot |
| TC17 | Medium | UR4, SR12 | Select Cancel on an active booking, dismiss the confirmation, then repeat and confirm it. | Dismissing leaves the booking unchanged; confirming changes the booking status to Cancelled. | Evidence of both confirmation outcomes |
| TC18 | High | UR6, UR7 | Change booking or room statuses and return to the dashboard. | Dashboard totals match the current room and booking records. | Dashboard and record comparison |
| TC19 | Medium | NFR1, NFR5 | Navigate through the application at normal and reduced browser widths. | Navigation remains clear and the main content remains usable. | Desktop and reduced-width screenshots |

---

## Planned Automated Testing

Automated testing is executed with pytest.

### Core Application Development coverage

| File | Planned Coverage |
|---|---|
| `tests/test_booking_service.py` | Booking rules, validation and booking-status behaviour |
| `tests/conftest.py` | Shared pytest fixtures and test configuration |

### Full regression coverage

The complete repository test run also includes:

- `tests/test_checkout_notifications.py`;
- `tests/test_notification_service.py`;
- `tests/test_telegram_command_service.py`.

These tests mainly support the later notification extension but also help confirm that it has not broken the original booking and check-out workflows.

Run the complete suite with:

```bash
pytest -q
```

The expected result is:

- all collected tests pass;
- no test-collection errors occur;
- no unexpected traceback is produced.

The actual pytest result must be recorded in `docs/test-results-template.md`.

---

## Test Data

Manual testing should use identifiable demonstration data:

- guest names beginning with `Test`;
- unique email addresses for valid guest tests;
- an existing email address for duplicate testing;
- unique room numbers;
- booking dates that do not conflict with unrelated records;
- one dedicated room for overlap and Maintenance tests.

Evidence should be captured before the related records are changed or removed.

The SQLite database should only be reset after confirming that no required evidence will be lost.

---

## Recording Results and Defects

Actual outcomes must be entered in `docs/test-results-template.md`.

Each completed result must include:

- test ID;
- related requirement or risk;
- expected result;
- actual result;
- Pass, Fail, Partial, Blocked or Not Run status;
- screenshot or automated evidence;
- defect ID where applicable.

A failed test must be recorded as a defect and repeated after correction. A defect should only be marked as fixed after the related test passes.

---

## Completion Criteria

Testing is complete when:

- all High-priority tests have recorded outcomes;
- every test has an appropriate status;
- important validation rules have supporting evidence;
- failed tests have been recorded and addressed;
- no unresolved Critical or High-severity defect prevents the core workflows;
- the traceability matrix has been updated;
- the final pytest suite completes successfully.