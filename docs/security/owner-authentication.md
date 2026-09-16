# Owner Authentication and Web Security

## Account model

`StaffAccount` stores a normalised email address, display name, scrypt password
hash, active flag, role and authentication timestamps. The initial roles are
`owner` and `staff`; every operational HTML route currently requires an active
account, while fine-grained role permissions remain deferred.

Passwords are never stored or logged in plaintext. New bootstrap passwords must
contain 14 to 128 characters. Authentication uses a dummy scrypt hash for
unknown accounts so the response path does not disclose whether an email exists.

`SecurityAuditEvent` records owner bootstrap, successful login, failed login and
logout outcomes. Failed attempts for unknown accounts do not retain the submitted
email or password. The table is an authentication audit trail and is separate
from the future booking-event history.

## Initial owner bootstrap

Apply migrations first, then run the one-time command:

```bash
flask --app app db upgrade
flask --app app bootstrap-owner
```

The interactive command hides and confirms the password. For controlled
non-interactive operation, provide `BOOTSTRAP_OWNER_EMAIL`,
`BOOTSTRAP_OWNER_NAME` and `BOOTSTRAP_OWNER_PASSWORD` through the process
environment. Never pass a password as a command-line argument. Unset bootstrap
values immediately after successful creation.

The command succeeds only when no staff account exists. Later account creation,
password reset and account recovery require a separately reviewed workflow.

## Request protection

- Flask-Login uses strong session protection and fresh, non-remembered logins.
- Authentication clears the previous session before establishing the user
  session, preventing reuse of pre-authentication session state.
- Redirects after login accept local absolute paths only.
- Every state-changing HTML form contains a Flask-WTF CSRF token.
- Login and protected internal API endpoints have configurable rate limits.
- The legacy API token uses constant-time comparison and remains environment-only.
- Sessions are HTTP-only, SameSite Lax, fixed to eight hours and secure in
  production.
- Responses set a restrictive content security policy, deny framing and MIME
  sniffing, disable unnecessary browser capabilities and prevent sensitive
  response caching. Production responses also enable HSTS.

## Current limits

The default rate-limit backend is process memory for simple local and single
process operation. A shared backend and reviewed proxy address handling are
required before horizontal scaling. Account recovery, password rotation,
multi-factor authentication, staff administration and fine-grained roles are
not implemented in this phase.
