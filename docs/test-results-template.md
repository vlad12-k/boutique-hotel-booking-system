# Test Results

This document records the outcomes of the manual and automated tests defined in `docs/testing-plan.md`.

The test identifiers, requirement links and expected outcomes correspond directly to the testing plan. This document adds the observed results, test status and available evidence.

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
| Manual test date | 14 June 2026 |
| Browser | Google Chrome and Safari on the local machine; exact versions were not recorded |
| Local URL | `http://127.0.0.1:5000` |
| Application command | `python app.py` |
| Automated test command | `pytest -q` |

---

## Test Status

| Status | Meaning |
|---|---|
| Pass | The actual result matched the expected result |
| Fail | The actual result did not match the expected result |
| Partial | The behaviour was observed, but part of the result or evidence still requires verification |
| Blocked | The test could not be completed because of another issue |
| Not Run | The planned test has not yet been completed |

---

## Manual Test Results

| Test ID | Requirement or Risk | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|---|
| TC01 | UR6, UR7 | The dashboard displays room counts, booking information and recent bookings without an application error. | The dashboard loaded successfully and displayed summary cards, today’s check-ins, today’s check-outs and recent booking activity. | Pass | Historical screenshot removed during privacy sanitisation |
| TC02 | UR2, UR6, SR6 | The original seeded rooms are displayed with room number, type, price and status. | The Rooms page loaded successfully and displayed room records with room number, type, price, status badges and update controls. | Pass | `screenshots/02-rooms-management.png` |
| TC03 | UR1, SR6 | A new guest is created and displayed on the Guests page. | The Add Guest form and Guests page were displayed successfully. However, the available evidence does not conclusively show the newly submitted guest appearing in the list. | Partial | Historical guest screenshots removed during privacy sanitisation |
| TC04 | UR1, SR13 | An invalid email address is rejected and the guest is not created. | The invalid email address was rejected and the application displayed a message requesting a valid email address. | Pass | `screenshots/07-invalid-email-validation.png` |
| TC05 | UR1, SR13 | A duplicate guest email is rejected and an appropriate message is displayed. | The duplicate email address was rejected and the application explained that a guest with the same email already existed. | Pass | `screenshots/08-duplicate-email-validation.png` |
| TC06 | UR2, SR6 | A new room is created and displayed on the Rooms page. | No completed test result confirming the creation of a new room was supplied. | Not Run | Additional evidence required |
| TC07 | UR4, SR7, SR8 | A valid booking is created and displays the correct total price. | The Add Booking form and Bookings page were displayed successfully. The available evidence shows booking records and total-price fields, but does not conclusively link a submitted test booking to its calculated total. | Partial | `screenshots/05-booking-creation.png`; historical booking record screenshot removed during privacy sanitisation |
| TC08 | UR9, SR8 | A booking with an invalid date range is rejected and a validation message is displayed. | The booking was rejected and the application stated that the check-out date must be after the check-in date. | Pass | `screenshots/10-invalid-booking-date.png` |
| TC09 | UR9, SR9 | An overlapping active booking is rejected and an overlap warning is displayed. | The overlapping booking was rejected because the selected room already had an active booking for the overlapping date range. | Pass | `screenshots/12-overlap-booking-prevention.png` |
| TC10 | UR9, SR10 | A room under Maintenance cannot be booked. | The booking was rejected and the application explained that rooms under Maintenance could not be booked. | Pass | `screenshots/11-maintenance-room-booking-prevention.png` |
| TC11 | SR8, SR12 | Client-side validation blocks missing or invalid booking dates and displays an inline message. | Invalid date behaviour was observed. However, the supplied evidence does not clearly distinguish client-side validation before submission from server-side validation after submission. | Partial | `screenshots/05-booking-creation.png`; `screenshots/10-invalid-booking-date.png` |
| TC12 | UR5, SR11 | Check-in changes the booking status to Checked-in and the room status to Occupied. | The selected booking changed to Checked-in and the room moved to Occupied. | Pass | `screenshots/15-check-in-result.png` |
| TC13 | UR5, SR11 | Check-out changes the booking status to Checked-out and the room status to Cleaning. | The selected booking changed to Checked-out and the room entered the Cleaning workflow. | Pass | `screenshots/16-check-out-result.png` |
| TC14 | UR3, SR11 | A room status change is saved and displayed correctly. | The room status was updated successfully and the changed status was displayed on the Rooms page. | Pass | `screenshots/03-room-status-update.png` |
| TC15 | UR8, SR12 | The room filter displays matching rooms and All restores the complete list without reloading. | The room filter displayed only rooms matching the selected status and restored the full list when All was selected. | Pass | `screenshots/03-room-filter.png` |
| TC16 | UR8, SR12 | The booking filter displays matching bookings and All restores the complete list without reloading. | The booking filter displayed only bookings matching the selected status and restored the full list when All was selected. | Pass | Historical screenshot removed during privacy sanitisation |
| TC17 | UR4, SR12 | Dismissing the cancellation confirmation leaves the booking unchanged, while confirming it cancels the booking. | A browser confirmation appeared before cancellation. The available evidence does not separately demonstrate both the dismissed and confirmed outcomes. | Partial | `screenshots/17-cancel-confirmation.png` |
| TC18 | UR6, UR7 | Dashboard totals match the current room and booking records. | The dashboard displayed room and booking totals, but a documented comparison with the final Rooms and Bookings records was not supplied. | Partial | Historical screenshot removed during privacy sanitisation |
| TC19 | NFR1, NFR5 | Navigation remains clear and the application remains usable at normal and reduced browser widths. | The main pages provided a consistent staff-facing interface and clear navigation. Reduced-width behaviour was not separately recorded. | Partial | Existing interface screenshots |

---

## Manual Test Summary

| Status | Number of Tests |
|---|---:|
| Pass | 12 |
| Partial | 6 |
| Not Run | 1 |
| Fail | 0 |
| Blocked | 0 |
| **Total** | **19** |

The Partial and Not Run statuses represent incomplete verification or missing evidence. They do not represent confirmed software failures.

---

## Automated Test Results

| Test ID | Test Area | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|---|
| AT01 | Complete pytest regression suite | All collected tests pass without collection errors or unexpected tracebacks. | The latest recorded test run completed with `34 passed`. | Pass | Terminal output from `pytest -q` |
| AT02 | Booking-service regression | Booking rules, validation and status behaviour pass the automated checks. | The booking-service tests were included in the successful complete test run. | Pass | `tests/test_booking_service.py`; AT01 result |
| AT03 | Notification-extension regression | Later notification functionality does not break the existing booking and check-out workflows. | The notification-related tests were included in the successful complete test run. | Pass | Related test files; AT01 result |

The complete pytest suite must be run once more after all final code changes. The result must be updated if the number of tests or their outcome changes.

---

## Defect Log

| Defect ID | Related Test | Description | Severity | Action Taken | Status |
|---|---|---|---|---|---|
| None | N/A | No confirmed software defects were recorded in the supplied test results. | N/A | N/A | Closed |

The Partial and Not Run results are evidence or verification gaps rather than confirmed application defects.

---

## Remaining Verification

Before final submission, the following tests require additional evidence or completion:

| Test ID | Required Action |
|---|---|
| TC03 | Capture the successfully created guest appearing in the Guests list |
| TC06 | Create a new room and capture the resulting room record |
| TC07 | Record one controlled booking and verify its calculated total price |
| TC11 | Capture the client-side inline validation before the form is submitted |
| TC17 | Record both dismissal and confirmation outcomes |
| TC18 | Compare dashboard totals directly with current room and booking records |
| TC19 | Record the application at a reduced browser width |
| AT01 | Run `pytest -q` again and retain the final terminal output |

All referenced screenshot filenames must also be checked against the actual contents of the `screenshots/` directory.

---

## Testing Notes

Manual testing was completed using the local Flask development server at `http://127.0.0.1:5000`.

The tests covered the main staff-facing workflows and business rules, including:

- dashboard display;
- guest validation;
- room management;
- booking validation;
- overlapping-booking prevention;
- Maintenance-room restrictions;
- check-in and check-out;
- status filtering;
- cancellation confirmation.

VS Code project-structure screenshots, source-code screenshots, Git status and GitHub pull-request evidence are development evidence rather than functional test results. They should be recorded in `docs/development-log.md` or the report appendix rather than in the manual test table.

---

## Conclusion

The completed results confirm that the main application pages loaded correctly and that the principal validation and workflow controls operated as expected.

Twelve manual tests passed, six require additional evidence or verification and one planned test has not yet been completed. No manual test was recorded as a confirmed failure.

The latest recorded automated result was:

```text
34 passed
```

The test record will be complete when the remaining verification items have been addressed, all evidence paths have been checked and the final pytest run has completed successfully.
