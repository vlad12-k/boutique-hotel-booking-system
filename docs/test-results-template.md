

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