# API Integration Overview

This project extends the boutique hotel booking system with an API-based housekeeping communication workflow. The extension combines external notification services, staff command handling and internal JSON audit endpoints so that housekeeping activity can be triggered, tracked and evidenced through API-based integrations.

## Integration Scope

The implemented API extension covers three connected areas:

1. **System-to-staff notifications**
   The hotel system sends housekeeping alerts when room operations require staff attention.

2. **Staff-to-system Telegram commands**
   Authorised staff can send Telegram bot commands to check room status, list cleaning tasks, mark rooms as ready, move rooms into maintenance and view recent notification logs.

3. **Audit and evidence endpoints**
   Notification outcomes are stored in the database and exposed through both a staff-facing log page and a JSON API endpoint.

## Selected External Services

| Service | Role in the system | Reason for selection |
|---|---|---|
| Telegram Bot API | Primary real-time housekeeping notification channel and staff command interface | Fast, low-cost, easy to demonstrate locally and suitable for operational staff alerts |
| Mailtrap SMTP Sandbox | Backup email delivery service for fallback testing | Safe testing environment that captures emails without sending them to real recipients |
| Internal JSON API | Audit evidence through `/api/notifications` and service status through `/api/health` | Supports testing, reporting and integration evidence without exposing credentials |

## Reason for API Selection

Telegram was selected as the primary communication channel because housekeeping alerts need to be fast and visible to staff. It also supports bot commands, which allowed the prototype to be extended from one-way alerts into a two-way staff operations workflow.

Mailtrap SMTP Sandbox was selected as the backup email service because it allows live SMTP integration testing without sending emails to real inboxes. This makes it suitable for academic evidence because the test email can be captured, inspected and screenshotted safely.

The JSON endpoints were retained as internal evidence APIs because they expose structured notification records that can be used to verify delivery outcomes, fallback behaviour and system health.

## Data Minimisation

Housekeeping notifications only include operational information such as:

- room number;
- cleaning task;
- room status;
- priority level;
- notification channel and result.

Guest names, phone numbers, payment details, identity documents and other unnecessary personal data are excluded from Telegram and email notification messages.

## Implemented Integration Points

The application includes the following API and workflow integration points:

| Integration point | Purpose |
|---|---|
| `POST /bookings/<booking_id>/checkout` | Updates a booking to `Checked-out`, moves the room to `Cleaning` and triggers a housekeeping notification |
| `POST /rooms/<room_id>/status` | Updates room status and triggers a room-ready notification when a room changes from `Cleaning` to `Available` |
| `GET /notifications` | Displays notification records in the staff-facing web interface |
| `GET /api/notifications` | Exposes notification log records as JSON for API testing and evidence |
| `GET /api/health` | Provides a simple health endpoint showing available API features |
| `telegram_bot_worker.py` | Runs the Telegram long-polling worker for staff commands |
| Telegram commands | Allow authorised staff to query and update room operations from Telegram |
| Mailtrap SMTP | Captures fallback housekeeping emails when Telegram delivery fails |

## Notification Workflow Summary

The notification workflow follows this sequence:

1. A room operation triggers a notification event.
2. The notification service builds a data-minimised operational message.
3. The system attempts primary Telegram delivery.
4. If Telegram delivery succeeds, the result is recorded with `channel=telegram`.
5. If Telegram delivery fails, the system attempts Mailtrap SMTP email fallback.
6. If email fallback succeeds, the result is recorded with `channel=email`.
7. If both channels fail, the result is recorded with `channel=failed`.
8. Staff can review the result through `/notifications` or `/api/notifications`.

## Telegram Staff Command Workflow

The Telegram staff bot adds a two-way workflow on top of the notification system. The Flask application runs the hotel web system, while `telegram_bot_worker.py` listens for Telegram updates and routes authorised commands to the command service.

Supported commands include:

| Command | Purpose |
|---|---|
| `/help` | Show available staff commands |
| `/status` | Return a live room status summary |
| `/cleaning` | List rooms currently waiting for housekeeping |
| `/available` | List available rooms |
| `/ready <room number>` | Mark a cleaned room as `Available` |
| `/maintenance <room number>` | Mark a room as `Maintenance` |
| `/notifications` | Return recent notification log entries |

Only chat IDs listed in `TELEGRAM_ALLOWED_CHAT_IDS` are allowed to use operational commands.

## Mailtrap Email Fallback Workflow

Mailtrap SMTP Sandbox is used to test backup email delivery. Real SMTP credentials are stored only in the local `.env` file, while `.env.example` contains safe placeholder values.

For the live fallback test, the primary Telegram channel was intentionally made unavailable. The system then attempted email fallback through Mailtrap SMTP. The fallback result was recorded in `/api/notifications` with `channel=email`, and the captured housekeeping email appeared in the Mailtrap Sandbox inbox.

## Current Test Evidence

The current evidence set includes:

- automated tests showing `12 passed`;
- `.env.example` showing secure Telegram and Mailtrap placeholder configuration;
- Telegram notification delivery screenshots;
- Telegram staff command bot screenshots;
- notification log screenshots;
- `/api/notifications` JSON audit screenshots;
- Mailtrap SMTP configuration evidence;
- Mailtrap inbox evidence showing the captured fallback email.

Automated tests currently verify that:

- housekeeping notification messages avoid guest personal data;
- room-ready messages avoid guest personal data;
- Telegram command parsing returns expected staff responses;
- email fallback is used when the primary Telegram API raises an error;
- checkout notification behaviour remains covered by the existing test suite.

## Limitations

The current implementation is suitable for local academic demonstration. In a production environment, the following improvements would be needed:

- replace Telegram long polling with a secure webhook or hosted worker;
- add retry handling and queueing for failed notifications;
- add staff authentication and role-based permissions;
- add production email provider verification instead of sandbox-only email testing;
- add monitoring and alerting for repeated API failures.