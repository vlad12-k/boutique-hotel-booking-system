# Notification Workflow Design

## Trigger Event

The workflow is triggered when reception staff check out a guest from a room.

## Workflow

1. Receptionist checks out a booking.
2. The booking status is updated.
3. The room status changes to Cleaning Required.
4. The system builds a housekeeping notification message.
5. The primary messaging API is called.
6. If the primary API fails, backup email delivery is attempted.
7. The notification result is saved in the notification log.
8. Reception staff can review the result in the notification log page.

## Message Payload

The notification message uses minimal operational data:

- Room number
- Cleaning task
- Room status
- Priority

The message does not include guest personal data.

## Error Handling

If the primary API fails because of missing credentials, network error or invalid token, the backup email channel is used. If both channels fail, the failure is recorded in the notification log.

## API Response Handling

The notification service returns a structured result containing:

- success state;
- delivery channel;
- notification message;
- error details;
- provider response details where available.

The checkout route uses this response to create a `NotificationLog` record. This means that every notification attempt can be reviewed after the check-out action, even when delivery fails.

## Fallback Logic

The workflow first attempts Telegram delivery as the primary notification channel. If Telegram credentials are missing, invalid, or the request fails, the system attempts backup email delivery.

If both channels fail, the booking and room status update still completes. The notification failure is stored in the notification log so reception or management staff can investigate the issue.

## Implemented Workflow Evidence

The implemented workflow follows this sequence:

1. `POST /bookings/<booking_id>/checkout` receives the check-out request.
2. The booking status changes to `Checked-out`.
3. The room status changes to `Cleaning`.
4. `send_housekeeping_notification()` builds a data-minimised message.
5. `telegram_service.py` attempts primary delivery.
6. `email_service.py` attempts backup delivery if the primary channel fails.
7. `NotificationLog` stores the final delivery result.
8. `/notifications` displays the log in the web interface.
9. `/api/notifications` exposes the log as JSON for API testing evidence.

## Security Design Notes

The design avoids sending guest personal data to housekeeping. The notification message uses room-level operational information only. API credentials are expected to be stored in environment variables and documented through `.env.example`, rather than hardcoded in the source code.