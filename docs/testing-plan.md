# Manual Testing Plan

| Test Case | Steps | Expected Result | Status |
|---|---|---|---|
| Add guest | Go to Guests → Add Guest, submit valid details | Guest appears in guest list | Not run |
| Add room | Go to Rooms → Add Room, submit valid room details | Room appears in room list | Not run |
| Create booking | Go to Bookings → Create Booking with valid guest, room and dates | Booking appears in booking list with total price | Not run |
| Invalid date validation | Create booking where check-out <= check-in | Error shown, booking not created | Not run |
| Overlapping booking validation | Create an active booking, then create another overlapping booking for same room | Clear overlap error shown, booking rejected | Not run |
| Maintenance room booking validation | Set room to Maintenance and try to book it | Error shown, booking rejected | Not run |
| Check-in | From bookings list, check in Pending/Confirmed booking | Booking becomes Checked-in, room becomes Occupied | Not run |
| Check-out | From bookings list, check out Checked-in booking | Booking becomes Checked-out, room becomes Cleaning | Not run |
| Room status update | In Rooms page, change room from Cleaning to Available | Room status updates successfully | Not run |
| Dashboard count check | Trigger status changes and review dashboard cards | Counts match current room/booking records | Not run |
