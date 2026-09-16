# Database Migration Runbook

## New local database

Set a synthetic local secret, then apply the schema:

```bash
cp .env.example .env
flask --app app db upgrade
```

To recreate the original academic demo inventory for local testing only:

```bash
flask --app app seed-academic-demo
```

The seed command aborts when any room already exists.

## PostgreSQL development database

Set `DATABASE_URL` to a disposable PostgreSQL database and run:

```bash
flask --app app db upgrade
flask --app app db current
```

Verify that revision `20260916_0001` is current. PostgreSQL must also contain the
`ex_booking_room_active_stay` exclusion constraint.

## Existing unversioned SQLite database

Do not run the initial migration directly against an existing database that was
created by the academic application's `create_all()` startup path; its tables
already exist.

1. Stop the application and make a private backup of the database file.
2. Inspect the tables and constraints against revision `20260916_0001`.
3. Resolve any schema or invalid-data differences explicitly.
4. Only after the schema is verified, mark it with:

```bash
flask --app app db stamp 20260916_0001
```

`stamp` records a revision without changing schema. It must never be used as a
substitute for verification or data migration.

## Production rule

Take a verified backup before every production migration. Apply migrations from
one release process, verify `flask --app app db current`, then start application
instances. A backup/restore retention process and a tested Render restore runbook
must be completed before deployment.
