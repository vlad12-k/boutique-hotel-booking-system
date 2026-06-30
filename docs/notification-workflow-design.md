# Notification Workflow Design

## Purpose

This document explains the notification workflow implemented in the boutique hotel booking system. The workflow connects room operations, external notification services and audit records so that housekeeping communication can be tested and evidenced as part of the API-focused unit work.

The workflow now supports three related notification paths:

1. **System-to-staff Telegram notifications** for housekeeping alerts.
2. **Mailtrap SMTP email fallback** when the primary Telegram channel is unavailable.
3. **Telegram staff command actions** for two-way room operations.

## Trigger Events

The notification workflow can be triggered by two main room operations.

| Trigger | System action | Notification behaviour |
|---|---|---|
| Guest check-out | Booking changes to `Checked-out` and room changes to `Cleaning` | Housekeeping alert is sent |
| Room status update | Room changes from `Cleaning` to `Available` | Room-ready notification is sent |

Telegram staff commands can also update room status directly and create audit log entries with `channel=telegram-command`.

## System-to-Staff Notification Workflow

The main notification workflow follows this sequence:

1. Reception staff complete a room operation.
2. The system updates the booking or room status.
3. The notification service builds a data-minimised operational message.
4. The system attempts primary Telegram Bot API delivery.
5. If Telegram delivery succeeds, the result is returned with `channel=telegram`.
6. If Telegram delivery fails, the system attempts Mailtrap SMTP email fallback.
7. If Mailtrap fallback succeeds, the result is returned with `channel=email`.
8. If both channels fail, the result is returned with `channel=failed`.
9. The final result is stored in the `NotificationLog` table.
10. Staff can review the record through `/notifications` and `/api/notifications`.

## Message Payload Design

Notification messages use only operational housekeeping data:

- room number;
- housekeeping task;
- room status;
- priority level.

The message design deliberately excludes guest personal data. Guest names, phone numbers, payment details, identity documents and other unnecessary personal data are not included in Telegram messages or fallback emails.

## Primary Telegram Delivery

Telegram Bot API is the primary notification channel because it supports fast staff alerts and operational bot commands. The system reads Telegram credentials from environment variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_housekeeping_chat_id
TELEGRAM_ALLOWED_CHAT_IDS=your_authorised_staff_chat_ids
TELEGRAM_POLL_INTERVAL_SECONDS=3
```

The notification service first calls the Telegram service. If Telegram succeeds, the notification log stores the result as `Sent` with `channel=telegram`.

## Mailtrap Email Fallback Delivery

Mailtrap SMTP Sandbox is used as the backup email channel. It captures fallback emails in a test inbox rather than sending them to real recipients.

Email credentials are read from environment variables:

```env
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USERNAME=your_mailtrap_username
EMAIL_PASSWORD=your_mailtrap_password
EMAIL_FROM=hotel-system@example.com
EMAIL_TO=housekeeping@example.com
```

When Telegram delivery raises an error, the notification service calls `send_backup_email()`. If Mailtrap SMTP delivery succeeds, the result is stored with `channel=email` and `status=Sent`. The result is also visible through `/api/notifications`.

## Telegram Staff Command Workflow

The Telegram staff command bot is a separate two-way workflow. It is run locally through:

```bash
python telegram_bot_worker.py
```

The worker receives Telegram updates, checks the incoming chat ID against `TELEGRAM_ALLOWED_CHAT_IDS`, routes valid commands to the command service and sends a reply back to Telegram.

Supported commands include:

| Command | Purpose |
|---|---|
| `/help` | Show available staff commands |
| `/status` | Return a live room status summary |
| `/cleaning` | List rooms waiting for housekeeping |
| `/available` | List available rooms |
| `/ready <room number>` | Mark a cleaned room as `Available` |
| `/maintenance <room number>` | Mark a room as `Maintenance` |
| `/notifications` | Return recent notification logs |

Room updates made through Telegram commands are recorded with `channel=telegram-command`.

## Error Handling

The workflow is designed to fail safely:

- if Telegram credentials are missing, invalid or unavailable, email fallback is attempted;
- if email credentials are missing or Mailtrap SMTP fails, the result is recorded as failed;
- room and booking status updates still complete even if notification delivery fails;
- error details are stored in the notification log for staff review;
- secrets are not exposed in JSON API responses or staff-facing pages.

## API Response Handling

The notification service returns a structured result containing:

- success state;
- delivery channel;
- notification message;
- error details;
- provider response details where available.

Routes use this result to create a `NotificationLog` record. This means every notification attempt can be reviewed after the operational action, even when delivery fails.

## Implemented Files

| File | Responsibility |
|---|---|
| `services/telegram_service.py` | Sends Telegram messages, receives Telegram updates and validates allowed chat IDs |
| `services/telegram_command_service.py` | Handles Telegram staff commands and room status updates |
| `services/email_service.py` | Sends Mailtrap SMTP fallback emails |
| `services/notification_service.py` | Coordinates Telegram primary delivery and Mailtrap email fallback |
| `telegram_bot_worker.py` | Runs the local Telegram command worker |
| `templates/notifications.html` | Displays notification records to staff |
| `app.py` | Triggers notifications and exposes `/notifications`, `/api/notifications` and `/api/health` |

## Evidence Mapping

The final evidence set demonstrates the workflow in three groups:

| Appendix group | Evidence focus |
|---|---|
| A1–A14 | Telegram housekeeping notification and JSON API evidence |
| A15.0–A15.12 | Telegram staff command bot workflow evidence |
| A16.1–A16.6 | Mailtrap SMTP email fallback evidence |

Automated tests now show `12 passed`, including tests for Telegram command handling and email fallback behaviour.

## Security Design Notes

The workflow uses environment variables for external service credentials. The local `.env` file contains real secrets and must not be committed. The committed `.env.example` file contains only placeholders.

The notification payload is intentionally limited to room-level operational data. This reduces privacy risk while still giving housekeeping staff enough information to complete their work.

## Production Limitations

The current design is suitable for local academic demonstration. A production implementation should consider:

- hosted worker or webhook deployment for Telegram;
- retry queue for failed notification attempts;
- production email provider and verified sending domain;
- authentication and role-based access for staff users;
- monitoring for repeated external API failures.