# API Integration Overview

This project extends the boutique hotel booking system with an API-based housekeeping notification workflow.

When reception staff check out a guest, the application updates the room status and sends a housekeeping alert through a primary messaging API. If the primary API fails, the system attempts backup email delivery and records the result in a notification log.

## Selected APIs

- Primary API: Telegram Bot API
- Backup API: SMTP email notification

## Reason for API Selection

The Telegram Bot API was selected because it supports instant operational notifications, is low-cost, and is suitable for a small hospitality prototype. Email was selected as a backup channel because it provides a written record and improves resilience if the primary notification method fails.

## Data Minimisation

Housekeeping notifications only include operational information such as room number, cleaning task, status and priority. Guest names, phone numbers, payment details and identity information are excluded.

## Implemented Integration Points

The application now includes the following API and workflow integration points:

- `POST /bookings/<booking_id>/checkout` updates the booking status, changes the room status to cleaning, and triggers the housekeeping notification workflow.
- `GET /notifications` displays the staff-facing notification log in the web interface.
- `GET /api/notifications` exposes notification log records as JSON for API testing and integration evidence.
- `GET /api/health` provides a simple service health endpoint for structural testing.

## Notification Workflow Summary

The notification workflow is triggered by the existing check-out action. After the booking is marked as checked out, the application builds a data-minimised housekeeping message and attempts to send it through the primary Telegram notification service. If the primary notification fails, the application attempts backup email delivery. The final result is stored in the `NotificationLog` table.

## Current Test Evidence

The notification workflow has been tested with missing Telegram and email credentials. The application handled this safely by recording a controlled failure in the notification log instead of crashing or exposing secrets.

Automated tests currently verify that:

- the health API endpoint returns a valid service status;
- the notification API endpoint returns a JSON list;
- housekeeping messages include room information;
- housekeeping messages avoid guest personal data such as names, phone numbers, passport information or payment details.