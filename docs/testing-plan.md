# Manual Testing Plan

| Test Case | Steps | Expected Result | Status |
|---|---|---|---|
| Add guest | Go to Guests → Add Guest, submit valid details | Guest appears in guest list | Not run |
| Add room | Go to Rooms → Add Room, submit valid room details | Room appears in room list | Not run |
| Create booking | Go to Bookings → Create Booking with valid guest, room and dates | Booking appears in booking list with total price | Not run |
| Invalid date validation | Create booking where check-out <= check-in | Error shown, booking not created | Not run |
| Overlapping booking validation | Create an active booking, then create another overlapping booking for same room | Clear overlap error shown, booking rejected | Not run |
| Maintenance room booking validation | Set room to Maintenance and try to book it | Error shown, booking rejected | Not run |
| Client-side booking date validation | Go to Bookings → Create Booking, try submit with missing check-in/check-out and with check-out earlier/same as check-in | Form is blocked with clear inline validation message before submit | Not run |
| Check-in | From bookings list, check in Pending/Confirmed booking | Booking becomes Checked-in, room becomes Occupied | Not run |
| Check-out | From bookings list, check out Checked-in booking | Booking becomes Checked-out, room becomes Cleaning | Not run |
| Room status update | In Rooms page, change room from Cleaning to Available | Room status updates successfully | Not run |
| Room status filtering (client-side) | In Rooms page, select each status filter option and then All | Only matching rows are shown for each status, All restores full list without page reload | Not run |
| Booking status filtering (client-side) | In Bookings page, select each status filter option and then All | Only matching booking rows are shown for each status, All restores full list without page reload | Not run |
| Cancel confirmation prompt | In Bookings page, click Cancel on an active booking and choose Cancel on browser confirm dialog, then retry and choose OK | First attempt keeps booking unchanged, second attempt cancels booking | Not run |
| Dashboard count check | Trigger status changes and review dashboard cards | Counts match current room/booking records | Not run |

# Manual Testing Plan

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This testing plan defines the manual tests that will be used to verify the main features, validation rules and user workflows of the hotel booking and room management application.

The plan supports the Unit 36 development portfolio by showing how the application will be tested against the original requirements and how evidence will be collected through screenshots and recorded results.

---

## Testing Scope

The testing scope covers the MVP features implemented in the Flask application:

- dashboard overview;
- guest management;
- room management;
- booking management;
- booking validation;
- check-in and check-out workflow;
- room status updates;
- vanilla JavaScript filtering;
- cancellation confirmation;
- basic usability review.

The testing scope does not cover production deployment, role-based login, payment processing or automated testing because these are outside the MVP scope.

---

## Test Environment

| Item | Details |
|---|---|
| Application | Boutique Hotel Booking and Room Management System |
| Framework | Python Flask |
| Database | SQLite |
| Browser | To be completed during testing |
| Operating System | macOS |
| Tester | Vladyslav Kononov |
| Local URL | `http://127.0.0.1:5000` |
| Run Command | `python app.py` |

---

## Testing Method

Manual functional testing will be used. Each test case will be executed through the browser as a normal staff user.

For each test, the tester should record:

- actual result;
- pass/fail status;
- screenshot evidence;
- any defect or unexpected behaviour.

Screenshot evidence should be saved in the `screenshots/` folder using clear file names.

---

## Test Priority Key

| Priority | Meaning |
|---|---|
| High | Core business workflow or important validation rule |
| Medium | Useful feature that improves usability or evidence quality |
| Low | Additional presentation or usability check |

---

## Test Cases

| Test ID | Priority | Requirement Link | Test Case | Steps | Expected Result | Status | Evidence |
|---|---|---|---|---|---|---|---|
| TC01 | High | UR6, SR8 | Dashboard loads | Open `/` in the browser. | Dashboard displays room counts, booking summary and recent activity. | Not run | `screenshots/01-dashboard.png` |
| TC02 | High | UR2, SR6 | Seeded rooms display | Open `/rooms`. | The 10 seeded hotel rooms are displayed with room number, type, price and status. | Not run | `screenshots/02-rooms-list.png` |
| TC03 | High | UR1, SR6 | Add guest | Go to Guests → Add Guest, enter valid guest details and submit. | Guest appears in the guest list. | Not run | `screenshots/03-add-guest.png` |
| TC04 | High | UR1, SR13 | Invalid guest email validation | Go to Guests → Add Guest and submit an invalid email address. | Error message is shown and guest is not created. | Not run | `screenshots/04-invalid-email.png` |
| TC05 | Medium | UR2, SR6 | Add room | Go to Rooms → Add Room, submit valid room details. | Room appears in the room list. | Not run | `screenshots/05-add-room.png` |
| TC06 | High | UR4, SR7 | Create booking | Go to Bookings → Create Booking with valid guest, room and dates. | Booking appears in the booking list with correct total price. | Not run | `screenshots/06-create-booking.png` |
| TC07 | High | UR9, SR8 | Invalid date validation | Create a booking where check-out date is the same as or before check-in date. | Error message is shown and booking is not created. | Not run | `screenshots/07-invalid-date.png` |
| TC08 | High | UR9, SR9 | Overlapping booking validation | Create an active booking, then create another overlapping active booking for the same room. | Clear overlap error is shown and the second booking is rejected. | Not run | `screenshots/08-overlap-validation.png` |
| TC09 | High | UR9, SR10 | Maintenance room booking validation | Set a room to Maintenance and try to book it. | Error message is shown and the booking is rejected. | Not run | `screenshots/09-maintenance-validation.png` |
| TC10 | High | UR9, SR12 | Client-side booking date validation | Go to Bookings → Create Booking and try to submit with missing dates or invalid date order. | Form is blocked with a clear inline validation message before submission. | Not run | `screenshots/10-client-date-validation.png` |
| TC11 | High | UR5, SR11 | Check-in | From the bookings list, check in a Pending or Confirmed booking. | Booking becomes Checked-in and room becomes Occupied. | Not run | `screenshots/11-check-in.png` |
| TC12 | High | UR5, SR11 | Check-out | From the bookings list, check out a Checked-in booking. | Booking becomes Checked-out and room becomes Cleaning. | Not run | `screenshots/12-check-out.png` |
| TC13 | High | UR3, SR6 | Room status update | In the Rooms page, change a room from Cleaning to Available. | Room status updates successfully. | Not run | `screenshots/13-room-status-update.png` |
| TC14 | Medium | UR8, SR12 | Room status filtering | In the Rooms page, select each status filter option and then All. | Only matching rows are shown for each status; All restores the full list without page reload. | Not run | `screenshots/14-room-filter.png` |
| TC15 | Medium | UR8, SR12 | Room filter empty state | Select a room status that currently has no matching rooms. | Empty-state message is displayed instead of a confusing blank table. | Not run | `screenshots/15-room-empty-filter.png` |
| TC16 | Medium | UR8, SR12 | Booking status filtering | In the Bookings page, select each status filter option and then All. | Only matching booking rows are shown for each status; All restores the full list without page reload. | Not run | `screenshots/16-booking-filter.png` |
| TC17 | Medium | UR8, SR12 | Booking filter empty state | Select a booking status that currently has no matching bookings. | Empty-state message is displayed if implemented. | Not run | `screenshots/17-booking-empty-filter.png` |
| TC18 | Medium | UR4, SR12 | Cancel confirmation prompt | In Bookings page, click Cancel on an active booking and choose Cancel in the browser dialog, then retry and choose OK. | First attempt keeps booking unchanged; second attempt cancels booking. | Not run | `screenshots/18-cancel-confirmation.png` |
| TC19 | Medium | UR6, SR8 | Dashboard count check | Trigger room and booking status changes, then review dashboard cards. | Dashboard counts match current room and booking records. | Not run | `screenshots/19-dashboard-counts.png` |
| TC20 | Low | NFR1 | Basic usability review | Navigate between Dashboard, Rooms, Guests and Bookings. | Navigation is clear and the application is understandable for staff users. | Not run | `screenshots/20-navigation-usability.png` |

---

## Defect Recording

Any failed or partially successful test should be recorded in the defect log below.

| Defect ID | Related Test ID | Description | Severity | Suggested Fix | Status |
|---|---|---|---|---|---|
| D01 | To be completed | To be completed | To be completed | To be completed | Open |

If no defects are found during final testing, replace the example row with:

| Defect ID | Related Test ID | Description | Severity | Suggested Fix | Status |
|---|---|---|---|---|---|
| None | N/A | No defects recorded during manual testing. | N/A | N/A | Closed |

---

## Screenshot Evidence Checklist

The following screenshots should be collected for the final report appendix:

1. Dashboard overview.
2. Rooms list.
3. Add guest form and successful guest creation.
4. Invalid guest email validation.
5. Add booking form.
6. Successful booking creation.
7. Invalid booking date validation.
8. Overlapping booking validation.
9. Maintenance room booking validation.
10. Check-in result.
11. Check-out result.
12. Room status update.
13. Room filtering.
14. Booking filtering.
15. Cancel confirmation.

---

## Testing Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Test data becomes inconsistent after repeated manual testing | Dashboard counts and booking statuses may become confusing | Use a clear test sequence and record screenshots immediately |
| Browser cache affects CSS or JavaScript display | UI may appear outdated during testing | Refresh browser and restart Flask server if needed |
| SQLite database contains old test records | Results may not match screenshots | Use consistent test data or reset database before final evidence capture |
| Missing screenshots | Weakens appendix evidence | Follow the screenshot checklist during testing |

---

## Testing Conclusion

To be completed after final manual testing.

Suggested wording after successful testing:

The manual testing confirmed that the main MVP workflows operated as expected. The application allowed staff to manage rooms, guests and bookings, prevented invalid booking dates, reduced double-booking risk, supported check-in and check-out workflows, and provided basic client-side filtering through vanilla JavaScript. The remaining limitations are suitable for future development and do not prevent the MVP from meeting its core academic and business objectives.