# Development Log

## Project

Boutique Hotel Booking and Room Management System

## Unit

Unit 36: Application Development

## Purpose

This development log records the main stages completed during the design, implementation, testing and refinement of the Boutique Hotel Booking and Room Management System.

It supports the Unit 36 development portfolio by demonstrating:

- an iterative development process;
- progression from requirements to implementation;
- changes made in response to testing and review;
- links between development work and project evidence;
- reflection on the outcome of each iteration.

The original Unit 36 project focused on guest, room and booking management. A later Unit 37 API-based housekeeping notification extension was added after the core application had been developed. That extension is identified separately in this log so that the scope of the two units remains clear.

---

## Development Approach

The project followed a lightweight iterative development approach.

This approach was appropriate because the application was an academic prototype for a small boutique hotel. The work could therefore be divided into controlled stages, with each iteration producing a usable improvement.

The main development stages were:

1. requirements analysis and initial design;
2. implementation of the Flask MVP;
3. interface and usability improvements;
4. code organisation and maintainability improvements;
5. documentation and traceability;
6. testing and correction;
7. final evidence and portfolio preparation;
8. later Unit 37 API extension.

Git and GitHub were used for version control. Branches and pull requests supported controlled development and allowed changes to be reviewed before they were incorporated into the main project.

---

## Iteration 1: Requirements Analysis and Design

### Goal

Define the business problem, user requirements, system requirements, data structure and main operational workflows before completing the application.

### Work completed

- Defined the business context for a 10-room boutique hotel.
- Identified the main operational users:
  - reception staff;
  - housekeeping staff;
  - hotel manager.
- Defined the original Unit 36 MVP scope.
- Identified functional and non-functional requirements.
- Defined supported room statuses:
  - Available;
  - Occupied;
  - Cleaning;
  - Maintenance.
- Defined supported booking statuses:
  - Pending;
  - Confirmed;
  - Checked-in;
  - Checked-out;
  - Cancelled.
- Designed the relationship between Guest, Room and Booking records.
- Designed the booking validation workflow.
- Designed the room and booking status lifecycles.
- Selected Flask, SQLAlchemy, SQLite, Jinja2, Bootstrap and vanilla JavaScript as the main technologies.

### Evidence

- `docs/requirements.md`
- `docs/design-diagrams.md`
- `docs/technical-notes.md`

### Outcome

The project began with a defined scope and a relational design that matched the business problem.

The requirements established that the system needed to:

- manage guests;
- manage rooms;
- create and manage bookings;
- prevent overlapping bookings;
- prevent bookings for rooms under Maintenance;
- coordinate check-in, check-out and room status updates;
- provide operational information through a dashboard.

### Reflection

Completing the requirements and diagrams before finalising the implementation reduced the risk of adding unrelated features.

The design also made it possible to connect later testing evidence directly to individual user and system requirements.

---

## Iteration 2: Initial Flask MVP

### Goal

Create the first working version of the staff-facing hotel booking and room management application.

### Work completed

- Created the Flask application structure.
- Configured the local SQLite database.
- Added Flask-SQLAlchemy.
- Created the `Guest`, `Room` and `Booking` models.
- Seeded 10 hotel rooms for demonstration and testing.
- Created the dashboard.
- Created the rooms page.
- Created the guests page.
- Created the bookings page.
- Created forms for adding:
  - guests;
  - rooms;
  - bookings.
- Added booking creation.
- Added booking cancellation.
- Added check-in and check-out actions.
- Added manual room-status updates.
- Added total-price calculation.
- Added validation for required booking information.
- Added validation to ensure that the check-out date is later than the check-in date.
- Added overlapping-booking prevention.
- Added prevention of bookings for rooms under Maintenance.

### Evidence

Core files:

- `app.py`
- `models.py`
- `templates/dashboard.html`
- `templates/rooms.html`
- `templates/guests.html`
- `templates/bookings.html`
- `templates/add_room.html`
- `templates/add_guest.html`
- `templates/add_booking.html`

Version-control evidence:

- GitHub branch: `copilot/create-boutique-hotel-app`
- Git commit and pull-request history

Local run command:

```bash
python app.py
```

### Outcome

A working MVP was produced.

The application supported the principal hotel workflows:

- creating guest records;
- viewing rooms;
- updating room status;
- creating bookings;
- preventing invalid bookings;
- checking guests in;
- checking guests out;
- cancelling bookings;
- viewing operational dashboard information.

### Reflection

This iteration demonstrated that Flask and SQLite were suitable for a local academic prototype.

The initial version solved the core business problem, but the interface still required improved presentation, filtering and clearer user feedback.

---

## Iteration 3: Interface and Vanilla JavaScript Improvements

### Goal

Improve usability and visual consistency without introducing a large frontend framework.

### Work completed

- Added `static/js/app.js`.
- Added client-side booking-date validation.
- Added room-status filtering.
- Added booking-status filtering.
- Added confirmation before booking cancellation.
- Improved the dashboard layout.
- Improved table presentation.
- Added clearer status presentation.
- Improved spacing and helper text.
- Improved form presentation.
- Refined `static/css/style.css`.
- Maintained a lightweight server-rendered architecture.
- Avoided unnecessary frontend frameworks such as React, Vue or Angular.

### Evidence

Implementation files:

- `static/js/app.js`
- `static/css/style.css`
- `templates/base.html`
- `templates/rooms.html`
- `templates/bookings.html`
- `templates/add_booking.html`

Screenshot evidence:

- `screenshots/02-rooms-management.png`
- `screenshots/03-room-filter.png`
- `screenshots/05-booking-creation.png`
- Historical dashboard, guest and booking record screenshots were removed during
  privacy sanitisation because they contained identifiable records.

### Outcome

The interface became clearer and more appropriate for non-technical hotel staff.

Room and booking filters allowed staff to locate relevant records more quickly. Client-side validation improved usability by identifying some invalid input before the form was submitted.

Server-side validation remained the authoritative protection because browser-side JavaScript can be bypassed.

### Reflection

Vanilla JavaScript was sufficient for the required interactions.

Using a larger frontend framework would have increased project complexity without providing a necessary benefit for the MVP.

---

## Iteration 4: Code Organisation and Maintainability

### Goal

Improve the organisation of reusable application logic and make important workflows easier to test.

### Work completed

- Added a `services/` package.
- Added `services/__init__.py`.
- Added `services/booking_service.py`.
- Moved reusable booking-related logic into a service module where appropriate.
- Retained Flask routes as the coordinators of browser requests, rendered templates and application workflows.
- Added a separate `tests/` folder.
- Added shared pytest configuration in `tests/conftest.py`.

### Evidence

- `services/__init__.py`
- `services/booking_service.py`
- `tests/conftest.py`
- `tests/test_booking_service.py`

### Outcome

The project structure became clearer by separating:

- database models;
- Flask routes;
- templates;
- static resources;
- reusable service logic;
- automated tests.

This improved maintainability and made important booking behaviour easier to verify independently.

### Reflection

Not every part of a small Flask prototype needs to be moved into a separate service.

The final structure therefore remains lightweight: Flask routes coordinate the web workflow, while reusable or independently testable logic can be placed in service modules.

---

## Iteration 5: Documentation and Traceability

### Goal

Create complete development, design, testing and user-support evidence for academic evaluation.

### Work completed

- Expanded the requirements specification.
- Created the application design diagrams.
- Created the development log.
- Created technical notes.
- Created the testing plan.
- Created the manual test-results document.
- Created the requirements traceability matrix.
- Created the user guide.
- Created peer-review evidence.
- Organised screenshot evidence.
- Linked requirements to implementation and testing evidence.
- Distinguished the original Unit 36 application from the later Unit 37 API extension.

### Evidence

- `docs/requirements.md`
- `docs/design-diagrams.md`
- `docs/development-log.md`
- `docs/technical-notes.md`
- `docs/testing-plan.md`
- `docs/test-results-template.md`
- `docs/traceability-matrix.md`
- `docs/user-guide.md`
- `docs/peer-review.md`
- `screenshots/`

### Outcome

The project became easier to evaluate because the design, implementation, requirements, testing and user guidance were recorded in separate documents.

The documentation also improved portfolio value because another developer or assessor can understand:

- why the system was created;
- how it is structured;
- how its main workflows operate;
- how it was tested;
- which improvements remain outside the MVP.

### Reflection

The first version of the documentation contained some repeated information and several sections still described completed work as planned.

The documentation was therefore reviewed and updated to reflect the final implementation rather than the earlier development state.

---

## Iteration 6: Testing and Correction

### Goal

Verify that the core workflows and later notification-related components behaved as expected without breaking the original booking application.

### Testing completed

Testing included:

- manual interface testing;
- booking-validation testing;
- room-status testing;
- booking-status testing;
- automated unit testing;
- automated workflow testing;
- notification-service testing;
- Telegram command-validation testing.

Automated test files include:

- `tests/test_booking_service.py`
- `tests/test_checkout_notifications.py`
- `tests/test_notification_service.py`
- `tests/test_telegram_command_service.py`

The recorded final pytest run reported:

```text
34 passed
```

### Main behaviours tested

- valid booking creation;
- invalid date rejection;
- overlapping-booking prevention;
- Maintenance-room restriction;
- total-price calculation;
- check-in status transition;
- check-out status transition;
- room status changes;
- notification workflow outcomes;
- Telegram staff-command validation;
- handling of unsuccessful notification delivery.

### Evidence

- `tests/`
- `docs/testing-plan.md`
- `docs/test-results-template.md`
- `docs/traceability-matrix.md`
- terminal pytest output
- application screenshots

Test command:

```bash
pytest -q
```

### Outcome

The automated test suite completed successfully in the recorded final run.

Testing provided evidence that the principal business rules worked and that the later notification extension did not remove the original booking functionality.

### Reflection

Automated testing was particularly valuable for business rules that could produce operational problems if implemented incorrectly, such as:

- overlapping bookings;
- invalid status transitions;
- incorrect room status;
- unsuccessful notification handling.

Manual testing remained necessary for visual layout, form usability, filtering and end-to-end staff interaction.

---

## Iteration 7: Final UI and Evidence Preparation

### Goal

Prepare the application for final academic submission and portfolio demonstration.

### Work completed

- Reviewed the shared page layout.
- Improved dashboard presentation.
- Improved table consistency.
- Improved room and booking status badges.
- Improved form usability.
- Captured the main application pages.
- Captured room-filter evidence.
- Captured booking-filter evidence.
- Reviewed documentation against the implemented project structure.
- Removed outdated planned-work statements from completed documentation.
- Separated Unit 36 evidence from Unit 37 API evidence.

### Evidence

- `screenshots/02-rooms-management.png`
- `screenshots/03-room-filter.png`
- `screenshots/05-booking-creation.png`
- Historical dashboard, guest and booking record screenshots were removed during
  privacy sanitisation because they contained identifiable records.

### Outcome

The application was presented as a coherent internal hotel operations system rather than only as an unfinished classroom prototype.

The screenshots, documentation and test evidence provide a clear record of the implemented functionality.

### Reflection

Visual presentation is important for usability and portfolio value, but it must not replace functional correctness.

The final work therefore balanced:

- interface quality;
- validation;
- maintainable structure;
- test evidence;
- documentation quality.

---

## Iteration 8: Separate Unit 37 API Extension

### Scope clarification

This iteration was completed after the original Unit 36 booking application and belongs primarily to Unit 37: Application Program Interfaces.

It is recorded here only to explain how the repository developed beyond the original MVP.

### Goal

Extend the check-out workflow with an API-based housekeeping notification process.

### Work completed

- Added Telegram housekeeping notifications.
- Added email fallback support.
- Added notification delivery logging.
- Added a notification records page.
- Added a Telegram staff-command worker.
- Added command validation.
- Added environment-variable configuration.
- Added automated tests for notification and command workflows.
- Added separate API, security and workflow documentation.

### Evidence

Implementation files:

- `telegram_bot_worker.py`
- `services/email_service.py`
- `services/notification_service.py`
- `services/telegram_service.py`
- `services/telegram_command_service.py`
- `templates/notifications.html`

Unit 37 documentation:

- `docs/api-design-diagrams.md`
- `docs/api-integration-overview.md`
- `docs/data-security-report.md`
- `docs/email-notification-workflow.md`
- `docs/notification-workflow-design.md`
- `docs/telegram-staff-bot-workflow.md`

### Outcome

The original booking system was extended with an automated housekeeping communication workflow while retaining the Unit 36 guest, room and booking functionality.

### Reflection

Keeping the API extension separate from the original application design makes the evidence easier to assess.

It shows progression from:

1. a working hotel management application;
2. to a system integrated with external communication services.

---

## Development Progress Summary

| Iteration | Focus | Status |
|---|---|---|
| Iteration 1 | Requirements analysis and design | Completed |
| Iteration 2 | Initial Flask MVP | Completed |
| Iteration 3 | UI and vanilla JavaScript improvements | Completed |
| Iteration 4 | Code organisation and maintainability | Completed |
| Iteration 5 | Documentation and traceability | Completed |
| Iteration 6 | Testing and correction | Completed |
| Iteration 7 | Final UI and evidence preparation | Completed |
| Iteration 8 | Separate Unit 37 API extension | Completed |

---

## Current Project Status

The project currently includes a working Flask application with:

- guest management;
- room management;
- booking management;
- booking validation;
- check-in and check-out;
- room status tracking;
- dashboard information;
- frontend filtering;
- responsive presentation;
- automated testing;
- supporting documentation;
- a separate API-based housekeeping notification extension.

The original Unit 36 MVP is complete for academic demonstration.

Guest record editing remains a possible future enhancement rather than an unfinished core requirement.

---

## Future Improvements

Possible future development includes:

- authenticated user accounts;
- role-based access control;
- editing existing guest records;
- a customer self-booking portal;
- online payment processing;
- production deployment;
- PostgreSQL or another production database;
- automated backups;
- advanced revenue and occupancy reporting;
- assignment of housekeeping tasks to named employees;
- expanded audit logging;
- broader browser and device testing.

These improvements are outside the completed academic MVP and do not prevent the current application from demonstrating the required Unit 36 functionality.

---

## Final Reflection

The iterative approach allowed the project to progress from a basic Flask prototype to a documented and tested hotel operations application.

The strongest aspects of the final project are:

- clear alignment with the hotel business problem;
- relational Guest, Room and Booking data;
- backend validation;
- overlap prevention;
- coordinated booking and room status updates;
- practical staff-facing interface;
- requirements traceability;
- automated testing;
- separation between the Unit 36 application and Unit 37 API extension.

The main limitation is that the application remains a local academic prototype without authentication, production deployment or advanced operational reporting.

However, within the defined MVP scope, the project successfully demonstrates planning, application design, implementation, testing, documentation and iterative improvement.
