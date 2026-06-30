

# Email Notification Workflow

## Purpose

This document explains the Mailtrap SMTP email fallback workflow added to the boutique hotel booking system. The email workflow supports the API-based housekeeping notification extension by providing a backup channel when the primary Telegram notification channel is unavailable.

The aim is not to send production customer emails. The aim is to demonstrate a safe external email service integration for operational housekeeping alerts and to provide testing evidence for the API-focused unit work.

## Selected Service

Mailtrap SMTP Sandbox was selected for email testing because it captures outgoing emails in a controlled test inbox instead of sending them to real recipients. This makes it suitable for local development, academic demonstration and screenshot evidence.

| Item | Implementation |
|---|---|
| Email service | Mailtrap SMTP Sandbox |
| SMTP host | `sandbox.smtp.mailtrap.io` |
| SMTP port | `2525` |
| Credential storage | Local `.env` file only |
| Safe template | `.env.example` with placeholder values |
| Evidence output | Captured email in Mailtrap Sandbox inbox |

## Environment Variables

The real SMTP credentials are stored only in the local `.env` file. The project repository includes `.env.example` with safe placeholder values.

```env
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USERNAME=your_mailtrap_username
EMAIL_PASSWORD=your_mailtrap_password
EMAIL_FROM=hotel-system@example.com
EMAIL_TO=housekeeping@example.com
```

The real `.env` file must not be committed to GitHub because it contains live credentials. Only `.env.example` should be committed.

## Implemented Code Files

| File | Responsibility |
|---|---|
| `services/email_service.py` | Reads SMTP configuration, builds an email message and sends it through Mailtrap SMTP |
| `services/notification_service.py` | Uses email fallback if Telegram delivery fails |
| `.env.example` | Documents required Mailtrap environment variables without exposing secrets |
| `tests/test_notification_service.py` | Tests that email fallback is used when Telegram raises an error |

## Email Fallback Flow

The fallback flow works as follows:

1. A room operation triggers a housekeeping notification.
2. The notification service builds a data-minimised operational message.
3. The system attempts primary Telegram delivery first.
4. If Telegram delivery fails, the system calls `send_backup_email()`.
5. `email_service.py` reads Mailtrap SMTP settings from environment variables.
6. The system sends the fallback email through Mailtrap SMTP.
7. The notification result is stored with `channel=email`.
8. The same record is visible in the staff notification log and `/api/notifications`.
9. The captured email appears in the Mailtrap Sandbox inbox.

## Trigger Used for Live Testing

The live fallback test used the existing room status workflow rather than adding a separate test-only endpoint. This avoided unnecessary API surface area and kept the evidence close to the real hotel workflow.

The tested sequence was:

1. A room was changed to `Cleaning`.
2. The same room was changed from `Cleaning` to `Available`.
3. This triggered the room-ready notification workflow.
4. The primary Telegram channel was intentionally unavailable for the test.
5. Mailtrap SMTP email fallback was used.
6. `/api/notifications` recorded the result as `channel=email` and `status=Sent`.
7. Mailtrap captured the fallback housekeeping email.

## Data Minimisation

The fallback email uses the same data-minimised message style as the Telegram notification workflow. It includes only operational housekeeping information:

- room number;
- housekeeping task;
- room status;
- priority level.

It does not include guest names, phone numbers, payment details, identity documents or booking-sensitive information.

## Testing Evidence

The evidence set for the email workflow includes:

| Appendix item | Evidence |
|---|---|
| A16.1 | Automated tests confirming email fallback notification behaviour |
| A16.2 | `.env.example` showing secure Mailtrap SMTP configuration placeholders |
| A16.3 | Mailtrap Sandbox SMTP credentials page with password hidden |
| A16.4 | JSON notification API showing `channel=email` and fallback error context |
| A16.5 | Mailtrap inbox showing the captured fallback housekeeping email |
| A16.6 | Mailtrap spam analysis or email diagnostic view, if included as optional evidence |

The automated test suite was updated from `10 passed` to `12 passed` after adding email fallback coverage.

## Validation Result

The final automated validation command was:

```bash
python -m py_compile app.py services/email_service.py services/notification_service.py services/telegram_service.py services/telegram_command_service.py telegram_bot_worker.py
pytest
```

The expected result is:

```text
12 passed
```

## Limitations

This email workflow is designed for local academic demonstration and safe sandbox testing. It does not yet provide production customer-facing booking confirmations.

Future improvements could include:

- production email domain verification;
- customer-facing booking confirmation emails;
- retry queue for failed notification delivery;
- staff role-based access control;
- monitoring for repeated Telegram or email delivery failures.