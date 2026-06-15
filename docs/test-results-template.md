

# Manual Test Results Template

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This document records the manual testing evidence for the hotel booking and room management application. It supports the Unit 36 development portfolio by showing how the implemented system was tested against functional requirements, validation rules and expected user workflows.

The table should be completed during testing. Each test should include the actual result, status and screenshot reference.

---

## Test Environment

| Item | Details |
|---|---|
| Application | Boutique Hotel Booking and Room Management System |
| Framework | Python Flask |
| Database | SQLite |
| Browser | To be completed |
| Operating System | macOS |
| Test Date | To be completed |
| Tester | Vladyslav Kononov |
| Run Command | `python app.py` |
| Local URL | `http://127.0.0.1:5000` |

---

## Test Status Key

| Status | Meaning |
|---|---|
| Pass | The feature worked as expected |
| Fail | The feature did not work as expected |
| Partial | The feature worked partly but needs improvement |
| Not Run | The test has not been completed yet |

---

## Manual Test Results

| Test ID | Requirement Link | Feature / Area | Test Steps | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|---|---|---|
| T01 | SR8, UR6 | Dashboard loads | Open `/` in the browser. | Dashboard loads and displays room and booking summary information. | To be completed | Not Run | Screenshot: `screenshots/01-dashboard.png` |
| T02 | SR1, SR6, UR2 | Seeded rooms display | Open `/rooms`. | 10 hotel rooms are displayed with room number, type, price and status. | To be completed | Not Run | Screenshot: `screenshots/02-rooms-list.png` |
| T03 | UR3, SR6 | Room status update | Change a room from Available to Maintenance, then save. | Room status updates successfully and the new status is shown on the Rooms page. | To be completed | Not Run | Screenshot: `screenshots/03-room-status-update.png` |
| T04 | UR1, SR6 | Add valid guest | Open `/guests/add`, enter valid guest details and submit. | Guest is saved and appears in the Guests list. | To be completed | Not Run | Screenshot: `screenshots/04-add-guest.png` |
| T05 | UR1, SR13 | Invalid guest email validation | Add a guest with an invalid email format. | System rejects the record and displays an error message. | To be completed | Not Run | Screenshot: `screenshots/05-invalid-email.png` |
| T06 | UR4, SR7 | Add valid booking | Open `/bookings/add`, select guest, room, valid dates and submit. | Booking is saved and appears in the Bookings list. | To be completed | Not Run | Screenshot: `screenshots/06-add-booking.png` |
| T07 | UR9, SR8 | Invalid booking date validation | Select a check-out date that is the same as or before the check-in date. | System rejects the booking and shows a validation message. | To be completed | Not Run | Screenshot: `screenshots/07-invalid-booking-date.png` |
| T08 | UR9, SR9 | Overlapping booking prevention | Create a second active booking for the same room and overlapping date range. | System rejects the booking and prevents double booking. | To be completed | Not Run | Screenshot: `screenshots/08-overlap-validation.png` |
| T09 | UR9, SR10 | Maintenance room booking prevention | Set a room to Maintenance and attempt to create a booking for that room. | System rejects the booking because the room is not available for use. | To be completed | Not Run | Screenshot: `screenshots/09-maintenance-room-validation.png` |
| T10 | UR5, SR11 | Guest check-in | Check in a Pending or Confirmed booking. | Booking status changes to Checked-in and room status changes to Occupied. | To be completed | Not Run | Screenshot: `screenshots/10-check-in.png` |
| T11 | UR5, SR11 | Guest check-out | Check out a Checked-in booking. | Booking status changes to Checked-out and room status changes to Cleaning. | To be completed | Not Run | Screenshot: `screenshots/11-check-out.png` |
| T12 | UR8, SR12 | Room status filter | Use the room status filter on the Rooms page. | Only rooms with the selected status are displayed. If no rows match, an empty-state message is shown. | To be completed | Not Run | Screenshot: `screenshots/12-room-filter.png` |
| T13 | UR8, SR12 | Booking status filter | Use the booking status filter on the Bookings page. | Only bookings with the selected status are displayed. If no rows match, an empty-state message is shown. | To be completed | Not Run | Screenshot: `screenshots/13-booking-filter.png` |
| T14 | UR4, SR12 | Cancel booking confirmation | Click Cancel on a booking. | Browser confirmation appears before the booking is cancelled. | To be completed | Not Run | Screenshot: `screenshots/14-cancel-confirmation.png` |
| T15 | NFR1 | Basic usability review | Navigate between Dashboard, Rooms, Guests and Bookings. | Navigation is clear and the application is understandable for staff users. | To be completed | Not Run | Screenshot: `screenshots/15-navigation-usability.png` |

---

## Defect Log

| Defect ID | Related Test | Description | Severity | Action Taken | Status |
|---|---|---|---|---|---|
| D01 | To be completed | To be completed | To be completed | To be completed | Open |

If no defects are found during testing, replace the example row with:

| Defect ID | Related Test | Description | Severity | Action Taken | Status |
|---|---|---|---|---|---|
| None | N/A | No defects recorded during manual testing. | N/A | N/A | Closed |

---

## Testing Notes

During final testing, each test should be completed in order and supported with screenshots. Screenshots should be stored in the `screenshots/` folder using clear file names that match the evidence column.

For the final report, the completed test table can be summarised in the main body and the screenshots can be included in the appendix as development and testing evidence.

---

## Testing Conclusion

To be completed after final manual testing.

Suggested final wording after successful testing:

The manual tests confirmed that the main workflows of the Boutique Hotel Booking and Room Management System worked as expected. The application allowed staff to manage rooms, guests and bookings, prevented invalid booking dates, reduced double-booking risk and supported check-in and check-out workflows. The remaining limitations are suitable for future development rather than critical MVP defects.
# Manual Test Results

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This document records the manual testing evidence for the hotel booking and room management application. It supports the development portfolio by showing how the implemented system was tested against functional requirements, validation rules and expected user workflows.

The tests focus on the main staff-facing workflows: dashboard review, room management, guest management, booking creation, validation, filtering, cancellation, check-in and check-out.

---

## Test Environment

| Item | Details |
|---|---|
| Application | Boutique Hotel Booking and Room Management System |
| Framework | Python Flask |
| Database | SQLite |
| Browser | Google Chrome / Safari on local machine |
| Operating System | macOS |
| Test Date | 14 June 2026 |
| Tester | Vladyslav Kononov |
| Run Command | `python app.py` |
| Local URL | `http://127.0.0.1:5000` |

---

## Test Status Key

| Status | Meaning |
|---|---|
| Pass | The feature worked as expected |
| Fail | The feature did not work as expected |
| Partial | The feature worked partly but needs improvement |
| Not Run | The test has not been completed yet |

---

## Manual Test Results

| Test ID | Requirement Link | Feature / Area | Test Steps | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|---|---|---|
| T01 | SR8, UR6 | Dashboard loads | Open `/` in the browser. | Dashboard loads and displays room and booking summary information. | Dashboard loaded successfully and displayed operational summary cards, today's check-ins, today's check-outs and recent booking activity. | Pass | Screenshot: `screenshots/01-dashboard.png` |
| T02 | SR1, SR6, UR2 | Seeded rooms display | Open `/rooms`. | Hotel rooms are displayed with room number, type, price and status. | Rooms page loaded successfully and displayed room records with room number, type, price, status badge and update controls. | Pass | Screenshot: `screenshots/02-rooms-page.png` |
| T03 | UR3, SR6 | Room status update | Change a room from Available to Cleaning or Maintenance, then save. | Room status updates successfully and the new status is shown on the Rooms page. | Room status was updated successfully and the changed status was visible on the Rooms page. | Pass | Screenshot: `screenshots/03-room-status-update.png` |
| T04 | UR8, SR12 | Room status filter | Use the room status filter on the Rooms page. | Only rooms with the selected status are displayed. If no rows match, an empty-state message is shown. | Room filtering worked correctly and only rooms matching the selected status were displayed. | Pass | Screenshot: `screenshots/04-room-filter.png` |
| T05 | UR1, SR6 | Guests page display | Open `/guests`. | Guest records are displayed with name, email, phone and notes. | Guests page loaded successfully and displayed the guest records in a clear table format. | Pass | Screenshot: `screenshots/05-guests-page.png` |
| T06 | UR1, SR6 | Add guest form display | Open `/guests/add`. | Add Guest form is displayed with fields for full name, email, phone and notes. | Add Guest form loaded successfully and displayed all expected input fields and guidance text. | Pass | Screenshot: `screenshots/06-add-guest-form.png` |
| T07 | UR1, SR13 | Invalid guest email validation | Add a guest with an invalid email format. | System rejects the record and displays an error message. | The invalid email was rejected and the system displayed an error message asking for a valid email address. | Pass | Screenshot: `screenshots/07-invalid-email-validation.png` |
| T08 | UR1, SR13 | Duplicate guest email validation | Add a guest using an email address that already exists. | System rejects the record and displays a duplicate email message. | The duplicate email was rejected and the system displayed a message explaining that a guest with the same email already exists. | Pass | Screenshot: `screenshots/08-duplicate-email-validation.png` |
| T09 | UR4, SR7 | Add booking form display | Open `/bookings/add`. | Add Booking form is displayed with guest, room, date and status fields. | Add Booking form loaded successfully and displayed guest selection, room selection, check-in date, check-out date and booking status fields. | Pass | Screenshot: `screenshots/09-add-booking-form.png` |
| T10 | UR9, SR8 | Invalid booking date validation | Select a check-out date that is the same as or before the check-in date. | System rejects the booking and shows a validation message. | The system rejected the booking and displayed a validation message stating that the check-out date must be after the check-in date. | Pass | Screenshot: `screenshots/10-invalid-booking-date.png` |
| T11 | UR9, SR10 | Maintenance room booking prevention | Set a room to Maintenance and attempt to create a booking for that room. | System rejects the booking because the room is not available for use. | The system rejected the booking and displayed a message explaining that rooms under Maintenance cannot be booked. | Pass | Screenshot: `screenshots/11-maintenance-room-booking-prevention.png` |
| T12 | UR9, SR9 | Overlapping booking prevention | Create a second active booking for the same room and overlapping date range. | System rejects the booking and prevents double booking. | The system rejected the overlapping booking and displayed a message explaining that the selected room already has an active booking for overlapping dates. | Pass | Screenshot: `screenshots/12-overlap-booking-prevention.png` |
| T13 | UR4, SR7 | Bookings page display | Open `/bookings`. | Bookings are displayed with guest, room, dates, status, total price and actions. | Bookings page loaded successfully and displayed booking records with guest, room, date range, status, total price and available actions. | Pass | Screenshot: `screenshots/13-bookings-page.png` |
| T14 | UR8, SR12 | Booking status filter | Use the booking status filter on the Bookings page. | Only bookings with the selected status are displayed. If no rows match, an empty-state message is shown. | Booking filtering worked correctly and only bookings matching the selected status were displayed. | Pass | Screenshot: `screenshots/14-booking-filter.png` |
| T15 | UR5, SR11 | Guest check-in | Check in a Pending or Confirmed booking. | Booking status changes to Checked-in and room status changes to Occupied. | The selected booking changed to Checked-in and the workflow confirmed that the room became occupied. | Pass | Screenshot: `screenshots/15-check-in-result.png` |
| T16 | UR5, SR11 | Guest check-out | Check out a Checked-in booking. | Booking status changes to Checked-out and room status changes to Cleaning. | The selected booking changed to Checked-out and the room status moved into the cleaning workflow. | Pass | Screenshot: `screenshots/16-check-out-result.png` |
| T17 | UR4, SR12 | Cancel booking confirmation | Click Cancel on a booking. | Browser confirmation appears before the booking is cancelled. | Browser confirmation appeared before cancellation, reducing the risk of accidental cancellation. | Pass | Screenshot: `screenshots/17-cancel-confirmation.png` |
| T18 | NFR1 | VS Code project structure review | Open the project in VS Code and review the project structure. | Main application files, templates, static assets, documentation and screenshots are organised clearly. | The project structure was clear and included `app.py`, `models.py`, `templates/`, `static/`, `docs/`, `screenshots/` and `README.md`. | Pass | Screenshot: `screenshots/18-vscode-project-structure.png` |
| T19 | NFR2 | Backend route review | Open `app.py` and review the implemented Flask routes. | Backend routes support dashboard, rooms, guests, bookings and booking workflows. | The route structure supported the main application workflows including dashboard, rooms, guests, bookings, add booking, check-in, check-out and cancellation. | Pass | Screenshot: `screenshots/19-vscode-app-routes.png` |
| T20 | NFR2 | Database model review | Open `models.py` and review the data models. | Guest, Room and Booking models support the required application data. | The data models provided a clear relationship between guests, rooms and bookings, with defined room and booking statuses. | Pass | Screenshot: `screenshots/20-vscode-models.png` |
| T21 | NFR1, NFR2 | Frontend files review | Open `style.css` or `app.js` and review frontend implementation. | Frontend files support polished styling, filtering, validation and interaction. | The frontend files contained custom styling and vanilla JavaScript for filtering, booking date validation and cancellation confirmation. | Pass | Screenshot: `screenshots/21-vscode-frontend-files.png` |
| T22 | NFR4 | Git working tree check | Run `git status` after committing and pushing the main changes. | Git reports a clean working tree. | Git reported that the branch was up to date and the working tree was clean. | Pass | Screenshot: `screenshots/22-terminal-git-clean.png` |
| T23 | NFR4 | Pull request evidence | Review the GitHub pull request for the polished application branch. | Pull request shows the branch, commit history and merge readiness. | GitHub pull request displayed the feature branch, changed files and commit summary. | Pass | Screenshot: `screenshots/23-github-pull-request.png` |
| T24 | NFR4 | Changed files review | Open the GitHub pull request `Files changed` tab. | Changed files are visible and demonstrate development work. | GitHub displayed the changed files, including updated templates, static assets, backend logic, README and documentation. | Pass | Screenshot: `screenshots/24-github-files-changed.png` |
| T25 | NFR4 | GitHub branch evidence | Open the repository branch on GitHub. | Repository branch displays latest committed project files. | GitHub branch displayed the updated project files and latest commit history. | Pass | Screenshot: `screenshots/25-github-branch.png` |

---

## Defect Log

| Defect ID | Related Test | Description | Severity | Action Taken | Status |
|---|---|---|---|---|---|
| None | N/A | No critical defects were recorded during final manual testing. | N/A | N/A | Closed |

---

## Testing Notes

Testing was completed manually using the local Flask development server. The application was launched with `python app.py` and accessed through `http://127.0.0.1:5000`.

The tests covered the main staff workflows and validation rules. Screenshots were captured for each test case and stored in the `screenshots/` folder using clear file names that match the evidence column. The screenshots provide evidence for both functional testing and development workflow review.

The GitHub and VS Code screenshots were included as additional evidence of development process, version control and project organisation.

---

## Testing Conclusion

The manual tests confirmed that the main workflows of the Boutique Hotel Booking and Room Management System worked as expected. The application allowed staff to manage rooms, guests and bookings, prevented invalid booking dates, reduced double-booking risk, blocked bookings for maintenance rooms and supported check-in and check-out workflows.

The dashboard, room management, guest management and booking management pages loaded successfully and provided a clear staff-facing interface. JavaScript enhancements supported filtering and cancellation confirmation, while backend validation protected key business rules.

No critical defects were recorded during final testing. The remaining limitations, such as role-based access control, guest editing, email confirmations, cloud deployment and advanced reporting, are suitable for future development rather than critical MVP defects.