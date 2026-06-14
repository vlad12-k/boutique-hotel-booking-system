## Project
Boutique Hotel Booking and Room Management System

## Purpose
This log records the main development iterations completed during the project. It supports the Unit 36 development portfolio by showing how the application was planned, built, reviewed and improved over time.

---

## Iteration 1: Initial Flask MVP

### Goal
Create the first working version of the staff-facing hotel booking and room management system.

### Work completed
- Created Flask application structure.
- Added SQLite database configuration.
- Added SQLAlchemy models for Guest, Room and Booking.
- Seeded 10 hotel rooms.
- Added dashboard page.
- Added room management page.
- Added guest management page.
- Added booking management page.
- Added booking creation workflow.
- Added check-in and check-out actions.
- Added room status update workflow.
- Added double booking validation.

### Outcome
A working MVP was created and merged into the main branch. The application can run locally using `python app.py`.

---

## Iteration 2: UI Polish and Vanilla JavaScript

### Goal
Improve the usability and visual presentation of the application while adding vanilla JavaScript frontend interactivity.

### Work completed
- Added `static/js/app.js`.
- Added client-side booking date validation.
- Added room status filtering.
- Added booking status filtering.
- Added confirmation before booking cancellation.
- Improved dashboard layout.
- Improved room and booking status presentation.
- Improved tables, spacing, helper text and visual consistency.

### Outcome
The application became clearer and more suitable for staff use. Vanilla JavaScript was used without frontend frameworks such as React, Vue or Angular.

---

## Iteration 3: Documentation and Testing Evidence

### Goal
Strengthen the project for academic submission and portfolio presentation.

### Work planned
- Create user guide.
- Create technical notes.
- Create test results template.
- Create traceability matrix.
- Record evidence for screenshots and testing.
- Link implemented features to user and system requirements.

### Outcome
To be completed after testing and evidence collection. (See <attachments> above for file contents. You may not need to search or read the file again.)


# Development Log

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This development log records the main development iterations completed during the project. It supports the Unit 36 development portfolio by showing how the application was planned, implemented, reviewed, improved and prepared for testing evidence.

The log also demonstrates an iterative development approach: each stage added value to the previous version, reduced project risk and improved alignment with the original business problem.

---

## Development Approach

The project followed a lightweight iterative methodology. This was suitable because the system is an academic prototype for a small boutique hotel and the requirements could be developed in short, controlled increments.

Each iteration focused on a specific improvement area:

1. building a working Flask MVP;
2. improving usability and frontend interaction;
3. strengthening documentation and testing evidence;
4. preparing the project for portfolio presentation and final evaluation.

Git and GitHub were used to manage versions, branches and pull requests. This provided evidence of controlled development and allowed changes to be reviewed before being merged.

---

## Iteration 1: Initial Flask MVP

### Goal
Create the first working version of the staff-facing hotel booking and room management system.

### Work completed
- Created the Flask application structure.
- Added SQLite database configuration.
- Added SQLAlchemy models for Guest, Room and Booking.
- Seeded 10 hotel rooms for demonstration and testing.
- Added dashboard page.
- Added room management page.
- Added guest management page.
- Added booking management page.
- Added booking creation workflow.
- Added check-in and check-out actions.
- Added room status update workflow.
- Added double-booking validation for active bookings.
- Added maintenance-room booking prevention.
- Added basic documentation files.

### Evidence
- GitHub branch: `copilot/create-boutique-hotel-app`
- Local run command: `python app.py`
- Main evidence: working Flask application and project structure

### Outcome
A working MVP was created and merged into the main branch. The application could run locally and supported the core workflows required for the hotel scenario.

### Reflection
This iteration proved that the main business problem could be solved with a simple web application. However, the interface still needed usability improvements, stronger documentation and clearer testing evidence.

---

## Iteration 2: UI Polish and Vanilla JavaScript

### Goal
Improve the usability and visual presentation of the application while adding frontend interactivity using vanilla JavaScript.

### Work completed
- Added `static/js/app.js`.
- Added client-side booking date validation.
- Added room status filtering.
- Added booking status filtering.
- Added confirmation before booking cancellation.
- Improved dashboard layout.
- Improved room and booking status presentation.
- Improved tables, spacing, helper text and visual consistency.
- Avoided frontend frameworks such as React, Vue and Angular.

### Evidence
- File: `static/js/app.js`
- Files: `templates/rooms.html`, `templates/bookings.html`, `templates/add_booking.html`
- Expected screenshots: room filter, booking filter and booking-date validation

### Outcome
The application became clearer and more suitable for staff use. The system remained lightweight because vanilla JavaScript was used instead of a frontend framework.

### Reflection
This iteration improved user experience, but the project still required stronger evidence for academic submission, including a traceability matrix, test template, user guide and technical notes.

---

## Iteration 3: Documentation and Testing Evidence

### Goal
Strengthen the project for academic submission, testing evidence and portfolio presentation.

### Work completed
- Created a development log.
- Created a user guide.
- Created technical notes.
- Created a manual test results template.
- Created a requirement traceability matrix.
- Linked implemented features to user and system requirements.
- Prepared the structure for screenshot evidence.

### Evidence
- File: `docs/development-log.md`
- File: `docs/user-guide.md`
- File: `docs/technical-notes.md`
- File: `docs/test-results-template.md`
- File: `docs/traceability-matrix.md`

### Outcome
The project became easier to evaluate because the development process, system features, testing plan and requirement coverage were documented.

### Reflection
This iteration is important for Unit 36 because the assignment assesses not only the final application but also the design, development process, support documentation, testing evidence and evaluation against requirements.

---

## Iteration 4: Planned Portfolio UI Polish

### Goal
Make the web application more visually professional and suitable for portfolio demonstration.

### Planned work
- Improve the shared page layout in `templates/base.html`.
- Improve the dashboard presentation.
- Improve table styling and status badges.
- Improve form pages for better usability.
- Refine `static/css/style.css` for a more polished visual identity.
- Ensure all pages look consistent and staff-friendly.

### Expected evidence
- Screenshot of dashboard.
- Screenshot of rooms page.
- Screenshot of bookings page.
- Screenshot of guest management page.
- Screenshot of add-booking workflow.

### Expected outcome
The application should look like a clean internal operations system rather than a basic classroom prototype.

---

## Iteration 5: Planned Functional Improvement

### Goal
Improve the system functionality by adding guest editing.

### Planned work
- Add an Edit Guest route in `app.py`.
- Add an `edit_guest.html` template.
- Add an Edit button to the Guests page.
- Reuse existing backend validation for guest email addresses.
- Update the user guide and traceability matrix.

### Reason
The current system allows staff to add and view guest records. Adding edit functionality would make guest management more complete and would strengthen the requirement coverage for guest record management.

---

## Summary of Development Progress

| Iteration | Focus | Status |
|---|---|---|
| Iteration 1 | Flask MVP | Completed |
| Iteration 2 | UI polish and vanilla JavaScript | Completed / being refined |
| Iteration 3 | Documentation and testing evidence | In progress |
| Iteration 4 | Portfolio UI polish | Planned |
| Iteration 5 | Guest editing workflow | Planned |

---

## Current Project Status

The project currently has a working Flask MVP with room, guest and booking management. The next priority is to finish the documentation branch, test the frontend filtering behaviour, improve the visual design and then add one functional improvement such as guest editing.

This staged approach helps keep the project stable while still improving the quality of the final submission and portfolio presentation.