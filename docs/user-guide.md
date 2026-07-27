# User Guide

This guide explains how hotel staff can use the Boutique Hotel Booking and Room Management System for daily room, guest and booking operations.

The application is a local staff-facing MVP. It does not include separate user accounts or role-based permissions.

The later Telegram and email housekeeping notification features are documented separately in the Application Program Interfaces documentation.

---

## 1. Starting the Application

From the project directory, start the Flask application with:

```bash
python app.py
```

Open the following address in a web browser:

```text
http://127.0.0.1:5000
```

The application opens on the Dashboard page.

---

## 2. Main Navigation

The navigation bar provides access to the main application areas.

| Page | Purpose |
|---|---|
| Dashboard | View current room and booking activity |
| Rooms | View rooms, filter them by status and update room status |
| Guests | View guest records and add new guests |
| Bookings | View, filter and manage booking records |

Forms for adding rooms, guests and bookings are accessed from their related pages.

---

## 3. Dashboard

The Dashboard provides an overview of current hotel operations.

It displays:

- total rooms;
- available rooms;
- occupied rooms;
- rooms being cleaned;
- rooms under Maintenance;
- today’s check-ins;
- today’s check-outs;
- recent bookings.

Staff can use the Dashboard at the beginning of the day to review room availability and expected guest activity.

---

## 4. Managing Rooms

Open the **Rooms** page to view all room records.

Each room includes:

- room number;
- room type;
- nightly price;
- current status.

### Room statuses

| Status | Meaning |
|---|---|
| Available | The room is ready for use |
| Occupied | A checked-in guest is using the room |
| Cleaning | The room requires preparation after check-out |
| Maintenance | The room has an operational issue and cannot be booked |

### Adding a room

1. Open the Rooms page.
2. Select **Add Room**.
3. Enter a unique room number.
4. Select or enter the room type.
5. Enter the nightly price.
6. Select the initial room status.
7. Submit the form.

The new room should appear on the Rooms page.

### Updating room status

1. Open the Rooms page.
2. Locate the required room.
3. Select a new status.
4. Submit the update.

After a guest checks out, the room automatically moves to `Cleaning`. When preparation is complete, staff can update it to `Available`.

### Filtering rooms

Use the status filter to display:

- All;
- Available;
- Occupied;
- Cleaning;
- Maintenance.

The filter updates the displayed rows without reloading the page.

---

## 5. Managing Guests

Open the **Guests** page to view stored guest records.

Each record may include:

- full name;
- email address;
- phone number;
- notes.

### Adding a guest

1. Open the Guests page.
2. Select **Add Guest**.
3. Enter the guest’s full name.
4. Enter a valid email address.
5. Enter the phone number.
6. Add optional notes.
7. Submit the form.

The application checks the email format and prevents duplicate guest email records.

The current MVP supports adding and viewing guests. Editing existing guest records remains a future improvement.

---

## 6. Managing Bookings

Open the **Bookings** page to view booking records.

Each booking displays:

- guest;
- room;
- check-in date;
- check-out date;
- booking status;
- total price;
- available actions.

### Booking statuses

| Status | Meaning |
|---|---|
| Pending | A pre-arrival booking awaiting further processing |
| Confirmed | A confirmed pre-arrival booking |
| Checked-in | The guest is currently staying in the room |
| Checked-out | The guest stay has been completed |
| Cancelled | The booking is no longer active |

---

## 7. Creating a Booking

1. Open the Bookings page.
2. Select **Add Booking**.
3. Select a guest.
4. Select a room.
5. Enter the check-in date.
6. Enter the check-out date.
7. Select the booking status.
8. Submit the form.

The application calculates the total price from the number of nights and the room’s nightly price.

### Booking validation

The application checks that:

- all required booking fields are completed;
- check-out is later than check-in;
- the selected room is not under Maintenance;
- the room does not have an overlapping active booking.

When validation fails, the booking is not created and an explanatory message is displayed.

---

## 8. Checking In a Guest

A Pending or Confirmed booking can be checked in.

1. Open the Bookings page.
2. Locate the eligible booking.
3. Select **Check In**.

After a successful check-in:

- the booking status changes to `Checked-in`;
- the room status changes to `Occupied`.

---

## 9. Checking Out a Guest

Only a Checked-in booking can be checked out.

1. Open the Bookings page.
2. Locate the Checked-in booking.
3. Select **Check Out**.

After a successful check-out:

- the booking status changes to `Checked-out`;
- the room status changes to `Cleaning`.

The room must be prepared and manually returned to `Available` before it is treated as ready for use.

---

## 10. Cancelling a Booking

1. Open the Bookings page.
2. Locate the relevant active booking.
3. Select **Cancel**.
4. Review the browser confirmation message.
5. Confirm the action.

Dismissing the confirmation leaves the booking unchanged. Confirming it changes the booking status to `Cancelled`.

---

## 11. Filtering Bookings

Use the booking-status filter to display:

- All;
- Pending;
- Confirmed;
- Checked-in;
- Checked-out;
- Cancelled.

The filter helps staff locate bookings by their current operational status without reloading the page.

---

## 12. Typical Staff Workflow

A normal booking lifecycle may follow these steps:

1. Staff review the Dashboard.
2. A guest record is created.
3. A room booking is created.
4. The guest arrives and is checked in.
5. The booking becomes `Checked-in`.
6. The room becomes `Occupied`.
7. The guest is checked out at the end of the stay.
8. The booking becomes `Checked-out`.
9. The room becomes `Cleaning`.
10. After preparation, staff return the room to `Available`.

---

## 13. Troubleshooting

| Problem | Likely Cause | Action |
|---|---|---|
| The application page does not load | The Flask server is not running | Run `python app.py` and reopen the local URL |
| A guest cannot be created | Required information is missing, the email is invalid or the email already exists | Review the validation message and correct the form |
| A booking is rejected | The dates are invalid, the room is under Maintenance or an overlapping booking exists | Review the message and change the dates or room |
| Check In is unavailable | The booking is not Pending or Confirmed | Review the current booking status |
| Check Out is unavailable | The booking is not Checked-in | Check the guest in before attempting check-out |
| A filter displays no records | No records match the selected status | Select All or another status |
| Frontend changes do not appear | The browser may be displaying cached resources | Refresh the page or restart the Flask application |

---

## 14. Current MVP Limitations

The current application does not include:

- authenticated user accounts;
- role-based permissions;
- guest-record editing;
- customer self-booking;
- online payments;
- cloud deployment;
- automated backups;
- advanced historical reporting.

These functions are retained as possible future improvements.

---

## Summary

The application allows hotel staff to:

- manage room and guest records;
- create validated bookings;
- prevent invalid or overlapping room reservations;
- check guests in and out;
- track room readiness;
- filter room and booking records;
- review current hotel activity from the Dashboard.