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
