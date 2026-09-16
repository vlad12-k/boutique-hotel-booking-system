# Production Foundation

## Purpose

This phase establishes a safe technical foundation for the Haifa Guest House
Operations App while preserving the verified academic workflows. It does not
claim that the application is production-ready or deployed.

## Application structure

`hotel_app.create_app()` is the composition root. It loads explicit
configuration, validates production requirements, initialises extensions,
registers the preserved routes and exposes explicit CLI commands. Importing the
application no longer creates tables or seeds records.

The root `app.py` and `models.py` modules remain as compatibility entry points so
existing commands and academic imports continue to work during the migration.

## Configuration contract

| Setting | Development | Production requirement |
|---|---|---|
| `APP_ENV` | `development` | `production` |
| `SECRET_KEY` | Required | At least 32 characters and not a known placeholder |
| `DATABASE_URL` | SQLite is supported locally | PostgreSQL through psycopg is required |
| Session cookie | HTTP-only, SameSite Lax | Secure flag is also required |

The application fails during startup when production configuration violates
these requirements. Secrets remain environment values and are never committed.

## Database authority and migrations

PostgreSQL is the production source of truth. Alembic migrations own schema
creation; application startup never calls `create_all()`.

The initial migration preserves the existing `guest`, `room`, `booking` and
`notification_log` tables. It adds date and non-negative-total checks. On
PostgreSQL, it also enables `btree_gist` and creates an exclusion constraint over
physical room and the half-open stay range `[check-in, check-out)`. The
constraint applies to Pending, Confirmed and Checked-in bookings.

Application validation still provides immediate staff feedback. The PostgreSQL
constraint is the final concurrency boundary: two transactions cannot commit
overlapping active bookings for the same physical room. Adjacent stays remain
valid.

## Domain contracts

Provider-neutral contracts define booking sources, lifecycle states, payment
states, room operational states, half-open stay periods, decimal money values
and external reservation references. A reservation adapter protocol defines the
boundary for future imports and providers.

These contracts are intentionally not yet persisted. Room types, staff accounts,
booking audit events and payments require reviewed additive migrations in later
phases. No SMS, Booking.com, Telegram, WhatsApp, email or payment provider is
implemented by this foundation.

## Inventory boundary

The original synthetic ten-room dataset remains available only through the
explicit `seed-academic-demo` command. It is never inserted automatically. The
real seven-room Haifa Guest House inventory is deferred until its commercial
room-type wording and starting operational data are approved.

## Verification

CI runs the complete regression suite on Python 3.12 with PostgreSQL 16. It
checks migrations, domain contracts, the preserved SQLite-compatible service
tests, the simultaneous last-room race, adjacent stays, dependency advisories
and repository secret patterns.

## Deferred work

- Owner authentication, CSRF, rate limiting and secure response headers.
- Persistent `StaffAccount`, `RoomType`, `Payment` and append-only booking-event
  models.
- The seven-room calendar, Today workflow, quick entry and database exports.
- Retention/anonymisation workflows and restore drills.
- Render Blueprint, paid resources, deployment and custom domain configuration.
- All external booking, notification and payment providers.
