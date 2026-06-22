# Data Security Report

## Guest Data Protection

The notification workflow uses data minimisation. Housekeeping staff only receive operational room information. The message does not include guest names, phone numbers, addresses, payment information or identity documents.

## API Credential Protection

API credentials are stored in environment variables and documented through `.env.example`. Real credentials must not be committed to the repository.

## Access Control

The check-out action should only be available to authorised reception or admin users. In a production system, this would be enforced through role-based access control.

## Transport Security

External API calls should use HTTPS. Telegram Bot API uses HTTPS endpoints. Email delivery should use TLS where SMTP is used.

## Logging

Notification logs store delivery status, channel, timestamp and error messages. Logs should not store API tokens or sensitive guest information.

## Remaining Risks

- Third-party API downtime
- Exposed API credentials
- Staff failing to act on notifications
- Email delivery delays
- Local development without production-grade authentication

## Recommended Improvements

- Add role-based authentication
- Add retry queue for failed notifications
- Add housekeeping confirmation button
- Add manager dashboard for unresolved cleaning tasks
- Rotate API credentials if exposure is suspected

## Evidence from Testing

A negative test was completed with no Telegram or email credentials configured. The system did not expose credentials, did not crash, and did not include guest personal data in the notification message. The failure was recorded in the notification log with operational details only.

The notification log showed that the application attempted the primary Telegram notification channel first and then attempted the backup email channel. Because neither set of credentials was configured in the local test environment, the final notification status was recorded as failed. This is expected behaviour for the negative security test.

## Security Controls Implemented

The current implementation includes the following security controls:

- API credentials are loaded from environment variables instead of being hardcoded in source files.
- `.env.example` documents the required configuration without exposing real secrets.
- Notification messages use room-level operational information only.
- Guest names, phone numbers, addresses, identity documents and payment data are excluded from housekeeping alerts.
- Notification failures are handled safely and logged instead of causing the application to crash.
- JSON API endpoints expose operational notification records but do not expose API tokens or email passwords.

## Security Test Summary

| Security Area | Test Performed | Result |
|---|---|---|
| Credential handling | Ran notification workflow without Telegram or email credentials | Controlled failure was logged; no secrets were exposed |
| Data minimisation | Reviewed generated housekeeping message | Message included room/task data only |
| Error handling | Triggered failed primary and backup notification channels | Application continued to update booking and room status |
| Logging | Checked notification log after checkout | Failure was recorded with channel, status, timestamp and error details |
| API exposure | Checked `/api/notifications` response | API returned operational records without credentials |

## Remaining Risks and Mitigation Plan

| Risk | Impact | Mitigation |
|---|---|---|
| Third-party notification API downtime | Housekeeping may not receive instant alerts | Keep backup email channel and consider retry queue |
| API credential exposure | Unauthorised messages could be sent | Store secrets in environment variables and rotate exposed credentials |
| Staff may miss notifications | Room cleaning could be delayed | Add housekeeping confirmation status and manager dashboard |
| Local prototype has limited authentication | Unauthorised users could trigger checkout in a production scenario | Add role-based authentication before production deployment |
| Error logs may grow over time | Logs may become difficult to review | Add log filtering, retention policy and admin review process |