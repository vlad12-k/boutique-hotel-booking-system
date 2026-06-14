

# User Guide

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This user guide explains how staff can use the Boutique Hotel Booking and Room Management System during daily hotel operations. It supports the Unit 36 development portfolio by providing user-facing documentation for the functional application.

The application is designed for internal hotel staff, including reception staff, housekeeping staff and a hotel manager. The MVP does not include separate user accounts or role-based login, but the workflows are described according to typical staff responsibilities.

---

## 1. Starting the Application

To run the application locally:

```bash
python app.py
```

Then open the local URL in a browser:

```text
http://127.0.0.1:5000
```

The application should open on the dashboard page.

---

## 2. Main Navigation

The navigation bar allows staff to move between the main areas of the system:

| Page | Purpose |
|---|---|
| Dashboard | View an overview of hotel activity and room status |
| Rooms | View rooms and update room status |
| Guests | View guest records and add new guests |
| Bookings | View bookings, cancel bookings, check guests in and check guests out |
| Add Booking | Create a new room booking |

---

## 3. Dashboard

The dashboard provides a quick operational overview for reception staff and managers.

The dashboard shows:

- total number of rooms;
- available rooms;
- occupied rooms;
- rooms being cleaned;
- rooms under maintenance;
- today's check-ins;
- today's check-outs;
- recent bookings.

### How staff use it

Reception staff can use the dashboard at the start of the day to understand which rooms are available, which rooms require cleaning and which guests are expected to arrive or leave.

Managers can use the dashboard to monitor daily hotel activity without opening each individual page.

---

## 4. Rooms Page

The Rooms page displays all hotel rooms and their current operational status.

Each room record includes:

- room number;
- room type;
- price per night;
- current room status.

Supported room statuses are:

| Status | Meaning |
|---|---|
| Available | Room is ready for a guest |
| Occupied | Guest is currently staying in the room |
| Cleaning | Room requires housekeeping before it can be used again |
| Maintenance | Room is not available because it requires repair or inspection |

### Updating room status

To update a room status:

1. Open the Rooms page.
2. Find the correct room.
3. Select the new status from the status dropdown.
4. Submit the status update.

Example: after a guest checks out, the system changes the room status to Cleaning. After housekeeping finishes, staff can update the room status back to Available.

### Filtering rooms

The Rooms page includes a status filter. Staff can filter by:

- All;
- Available;
- Occupied;
- Cleaning;
- Maintenance.

The filter uses vanilla JavaScript and does not require the page to reload. If no rooms match the selected filter, an empty-state message is displayed.

---

## 5. Guests Page

The Guests page displays guest records stored in the system.

Each guest record includes:

- full name;
- email address;
- phone number;
- notes, if entered.

### Adding a guest

To add a guest:

1. Open the Guests page.
2. Click Add Guest.
3. Enter the guest's full name.
4. Enter the guest's email address.
5. Enter the guest's phone number.
6. Add notes if needed.
7. Submit the form.

The system checks that required fields are completed and that the email address has a basic valid format.

### Current limitation

The current MVP allows staff to add and view guests. Editing guest records is planned as a future improvement.

---

## 6. Bookings Page

The Bookings page displays booking records and allows staff to manage the booking lifecycle.

Each booking record includes:

- guest name;
- room number;
- check-in date;
- check-out date;
- booking status;
- total price;
- available actions.

Supported booking statuses are:

| Status | Meaning |
|---|---|
| Pending | Booking has been created but not fully confirmed |
| Confirmed | Booking is confirmed |
| Checked-in | Guest has arrived and is staying in the room |
| Checked-out | Guest has left and the stay is complete |
| Cancelled | Booking has been cancelled |

---

## 7. Creating a Booking

To create a booking:

1. Open the Bookings page.
2. Click Add Booking or Create Booking.
3. Select the guest.
4. Select the room.
5. Choose a check-in date.
6. Choose a check-out date.
7. Select the booking status.
8. Submit the form.

The system calculates the total price based on the room price and the number of nights.

### Booking validation

The system prevents common booking problems:

| Validation Rule | Purpose |
|---|---|
| Check-out date must be after check-in date | Prevents invalid date ranges |
| Room must not already have an active overlapping booking | Reduces double-booking risk |
| Room must not be under Maintenance | Prevents unusable rooms from being assigned to guests |
| Required fields must be completed | Prevents incomplete records |

The date validation is supported by both backend validation and vanilla JavaScript frontend validation.

---

## 8. Checking a Guest In

To check in a guest:

1. Open the Bookings page.
2. Find a Pending or Confirmed booking.
3. Click the Check-in action.

After check-in:

- the booking status changes to Checked-in;
- the room status changes to Occupied.

This helps reception staff and housekeeping staff understand that the room is currently in use.

---

## 9. Checking a Guest Out

To check out a guest:

1. Open the Bookings page.
2. Find a Checked-in booking.
3. Click the Check-out action.

After check-out:

- the booking status changes to Checked-out;
- the room status changes to Cleaning.

This supports the housekeeping workflow because the room is clearly marked as needing cleaning before it becomes available again.

---

## 10. Cancelling a Booking

To cancel a booking:

1. Open the Bookings page.
2. Find the relevant booking.
3. Click Cancel.
4. Confirm the action in the browser confirmation dialog.

The confirmation prompt helps reduce accidental cancellations.

---

## 11. Filtering Bookings

The Bookings page includes a booking status filter.

Staff can filter by:

- All;
- Pending;
- Confirmed;
- Checked-in;
- Checked-out;
- Cancelled.

This feature helps staff quickly find bookings by operational status. It is implemented using vanilla JavaScript.

---

## 12. Common Staff Workflow Example

A typical daily workflow may look like this:

1. Reception opens the dashboard to review today's activity.
2. Reception adds a new guest record.
3. Reception creates a booking for the guest.
4. On arrival day, reception checks the guest in.
5. The room status automatically becomes Occupied.
6. On departure day, reception checks the guest out.
7. The room status automatically becomes Cleaning.
8. Housekeeping cleans the room.
9. Staff update the room status back to Available.

This workflow shows how the application supports coordination between reception and housekeeping.

---

## 13. Troubleshooting

| Problem | Possible Cause | Suggested Action |
|---|---|---|
| Page does not load | Flask server may not be running | Run `python app.py` and open `http://127.0.0.1:5000` |
| New guest is not saved | Required fields may be missing or email may be invalid | Check the form fields and try again |
| Booking is rejected | Dates may be invalid, room may be under Maintenance or room may already be booked | Review the error message and select different dates or room |
| Filter shows no rows | No records match the selected status | Select All or another status |
| JavaScript changes not visible | Browser cache may show old files | Refresh the browser or restart Flask server |

---

## 14. Current MVP Limitations

The current version is an academic MVP and has some limitations:

- no separate login for receptionist, housekeeping and manager roles;
- no guest editing yet;
- no customer-facing online booking portal;
- no payment processing;
- no email or SMS confirmations;
- no cloud deployment;
- no automated backups;
- no advanced reporting dashboard.

These limitations are suitable future improvements and can be discussed in the final evaluation.

---

## 15. User Guide Summary

The application provides the main tools needed for a small hotel to manage rooms, guests and bookings. It supports the core staff workflows of adding guests, creating bookings, checking guests in, checking guests out and updating room status.

The system also includes validation rules to reduce double bookings and invalid records. This makes it more reliable than a manual spreadsheet or paper-based workflow for the boutique hotel scenario.