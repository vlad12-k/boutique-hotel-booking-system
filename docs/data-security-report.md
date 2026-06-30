# Data Security Report

## Purpose

This document explains the data security controls used in the boutique hotel booking system API extension. The extension integrates Telegram Bot API, a Telegram staff command worker, Mailtrap SMTP Sandbox email fallback and internal JSON audit endpoints.

The security design focuses on safe credential handling, data minimisation, controlled error handling and evidence that external service failures do not expose secrets or guest personal data.

## Data Processed by the Notification Workflow

The notification workflow uses only operational housekeeping data.

| Data item | Used in notification? | Reason |
|---|---:|---|
| Room number | Yes | Housekeeping needs to know which room requires work |
| Room status | Yes | Staff need to know whether a room is `Cleaning`, `Available` or `Maintenance` |
| Housekeeping task | Yes | Staff need the operational task description |
| Priority level | Yes | Staff need to understand urgency |
| Guest name | No | Not required for housekeeping notification |
| Guest phone number | No | Not required for housekeeping notification |
| Guest address | No | Not required for housekeeping notification |
| Payment details | No | Not required and would create unnecessary privacy risk |
| Identity documents | No | Not required and would create unnecessary privacy risk |

This keeps Telegram messages and Mailtrap fallback emails data-minimised.

## Credential Protection

External service credentials are loaded from environment variables rather than being hardcoded in source files.

The local `.env` file stores real credentials and must not be committed to GitHub. The committed `.env.example` file contains only safe placeholder values.

Credential categories include:

| Credential group | Purpose | Storage approach |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Sends Telegram messages and staff command replies | Local `.env` only |
| `TELEGRAM_CHAT_ID` | Outbound housekeeping notification chat | Local `.env` only |
| `TELEGRAM_ALLOWED_CHAT_IDS` | Authorised staff command access list | Local `.env` only |
| `EMAIL_USERNAME` | Mailtrap SMTP username | Local `.env` only |
| `EMAIL_PASSWORD` | Mailtrap SMTP password | Local `.env` only |
| `EMAIL_FROM` and `EMAIL_TO` | Test email sender and recipient values | Local `.env`, placeholders in `.env.example` |

The repository should contain `.env.example`, but it must not contain `.env`.

## Access Control

The Telegram staff command bot uses chat ID allow-listing. Incoming Telegram messages are checked against `TELEGRAM_ALLOWED_CHAT_IDS` before operational commands are processed.

This prevents unknown Telegram chats from using commands such as:

- `/ready <room number>`;
- `/maintenance <room number>`;
- `/notifications`.

The web application remains a local academic prototype. In production, web routes such as check-out and room status updates would require user authentication and role-based permissions.

## Transport Security

Telegram Bot API requests are sent to HTTPS Telegram endpoints. Mailtrap SMTP fallback uses SMTP with STARTTLS through the configured SMTP port.

The local Flask development server is suitable for academic demonstration only. It should not be used as a production deployment server.

## Logging and Audit Records

Notification outcomes are stored in the `NotificationLog` table. Logs include operational delivery information such as:

- room reference;
- notification channel;
- delivery status;
- notification message;
- error message;
- timestamp.

The logs do not store Telegram bot tokens, Mailtrap SMTP passwords or guest-sensitive data.

The same audit information is available through:

- `/notifications` for staff-facing review;
- `/api/notifications` for JSON API evidence.

## Error Handling

The notification workflow fails safely:

1. The system attempts primary Telegram delivery.
2. If Telegram fails, Mailtrap SMTP email fallback is attempted.
3. If Mailtrap succeeds, the result is recorded with `channel=email` and `status=Sent`.
4. If both delivery channels fail, the result is recorded with `channel=failed`.
5. Room and booking status updates still complete even when notification delivery fails.

This means operational actions are not blocked by external API failure, while delivery issues remain visible in the notification log.

## Evidence from Testing

The final evidence set includes positive, fallback and automated test evidence.

| Evidence group | Security relevance |
|---|---|
| A1–A14 | Telegram notification workflow and JSON audit records |
| A15.0–A15.12 | Telegram staff command bot workflow and authorised command evidence |
| A16.1–A16.6 | Mailtrap SMTP fallback configuration, JSON audit and captured email evidence |

The automated test suite was updated to show `12 passed`. The tests cover:

- data-minimised housekeeping messages;
- room-ready messages without guest personal data;
- Telegram command service behaviour;
- email fallback when Telegram raises an error.

## Security Controls Implemented

The current implementation includes the following controls:

- API and SMTP credentials are loaded from environment variables.
- `.env.example` documents configuration using placeholders only.
- Real `.env` credentials are excluded from GitHub.
- Telegram staff commands are restricted through allowed chat IDs.
- Notification messages use operational room data only.
- Guest personal data is excluded from Telegram and email messages.
- Failed Telegram delivery can fall back to Mailtrap SMTP email.
- Notification outcomes are logged for review and audit evidence.
- JSON API responses expose operational records but not secrets.

## Security Test Summary

| Security area | Test performed | Result |
|---|---|---|
| Credential handling | Reviewed `.env.example` and local setup approach | Real credentials stay in `.env`; placeholders are committed |
| Data minimisation | Reviewed generated Telegram and email notification messages | Messages contained room/task/status data only |
| Telegram primary delivery | Triggered housekeeping notification workflow | Successful Telegram delivery was logged as `channel=telegram` |
| Telegram command access | Used authorised Telegram chat commands | Valid commands were processed and logged as `telegram-command` |
| Email fallback | Made Telegram unavailable and triggered room-ready notification | Mailtrap fallback email was captured and logged as `channel=email` |
| JSON audit exposure | Checked `/api/notifications` | API returned operational records without tokens or SMTP passwords |
| Automated tests | Ran full test suite | `12 passed` |

## Remaining Risks and Mitigation Plan

| Risk | Impact | Mitigation |
|---|---|---|
| Telegram API downtime | Housekeeping may not receive instant Telegram alerts | Keep Mailtrap/email fallback and add retry queue in future |
| Mailtrap or SMTP failure | Backup email may not be captured | Log failures and add retry/queue handling in future |
| API credential exposure | Unauthorised messages could be sent | Store secrets in `.env`, avoid committing `.env`, rotate exposed credentials |
| Staff may miss notifications | Room cleaning could be delayed | Add housekeeping acknowledgement and manager dashboard |
| Local prototype has limited web authentication | Unauthorised web users could trigger operations in production | Add login, role-based access and audit trail before deployment |
| Long-polling worker runs locally | Telegram command bot depends on a local process | Use hosted worker or webhook for production |
| Logs may grow over time | Logs may become difficult to review | Add filtering, retention policy and admin review process |

## Production Recommendations

Before production deployment, the system should add:

- staff authentication and role-based authorisation;
- hosted Telegram webhook or managed worker process;
- verified production email domain rather than sandbox-only email testing;
- retry queue for failed external API calls;
- monitoring for repeated Telegram or SMTP failures;
- log retention and privacy review policy;
- HTTPS deployment behind a production WSGI server.