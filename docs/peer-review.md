# Peer Review Log

| Reviewed Area | Feedback Received | Interpretation | Action Taken |
|---|---|---|---|
| (Placeholder) | (Placeholder) | (Placeholder) | (Placeholder) |

# Peer Review Log

## Project
Boutique Hotel Booking and Room Management System

## Purpose
This peer review log records feedback received during the development of the hotel booking and room management application. It supports the Unit 36 development portfolio by showing how feedback was interpreted and how improvements were planned or implemented.

Peer review is important because it helps identify usability issues, missing functionality, unclear documentation and technical risks before the final evaluation stage.

---

## Review Context

The application was reviewed as an academic prototype for a small 10-room boutique hotel. The review focused on whether the system was suitable for internal hotel staff, especially reception staff, housekeeping staff and a manager.

The reviewed version included:

- dashboard overview;
- room management;
- guest management;
- booking management;
- check-in and check-out workflow;
- room status updates;
- booking validation;
- vanilla JavaScript filtering and confirmation features.

---

## Peer Review Summary

| Reviewed Area | Feedback Received | Interpretation | Action Taken / Planned |
|---|---|---|---|
| Dashboard | The dashboard gives a useful overview, but it should look more professional for presentation. | The dashboard works functionally, but the visual design needs improvement to make it suitable for portfolio evidence. | Planned: improve dashboard cards, spacing, headings and visual hierarchy in the UI polish iteration. |
| Room management | Room statuses are clear, but filtering should show a message when no rooms match the selected status. | A blank table may confuse staff because it does not explain why no rows are visible. | Implemented: added an empty-state message for the room status filter. |
| Booking management | The booking table is useful, but filtering should also include an empty-state message. | The booking page should behave consistently with the rooms page. | Planned: add `bookingFilterEmptyMessage` to the bookings template. |
| Booking validation | The system correctly prevents invalid dates and overlapping bookings, but evidence should be captured. | Validation is a key part of the business problem and must be shown clearly in testing evidence. | Planned: capture screenshots for invalid dates, overlapping bookings and maintenance-room booking prevention. |
| Guest management | The system allows guests to be added and viewed, but there is no edit function. | Guest records may need correction after entry; this is a realistic staff requirement. | Planned: add an Edit Guest workflow in a later functional improvement branch. |
| User interface | The system is simple to use, but some pages still look like a basic prototype. | The application needs a more consistent and professional visual identity. | Planned: improve `base.html`, dashboard, tables, forms and `style.css`. |
| Documentation | The documentation structure is useful, but it needs more detail for assessment evidence. | The project needs stronger support documentation for the development portfolio. | Implemented / in progress: development log, user guide, technical notes, traceability matrix and test results template. |
| Testing evidence | Manual tests are planned, but actual results and screenshots still need to be added. | The final report should include proof that the system was tested against requirements. | Planned: complete test results table and add screenshots to the appendix. |

---

## Key Feedback Themes

### 1. Improve presentation quality

The application is functional, but the visual design should be improved so it looks like a professional internal operations tool. This is important for both the academic submission and future portfolio use.

### 2. Strengthen evidence

The project should not only claim that features work. It should include screenshots, manual test results and references to the relevant files or pages.

### 3. Make workflows clearer

The check-in, check-out and room status workflows are useful, but the report and documentation should clearly explain how they support daily hotel operations.

### 4. Add one realistic functional improvement

Adding guest editing would improve the system because hotel staff may need to correct guest details after the initial record is created.

---

## Improvements Implemented from Review

| Improvement | Reason | Related File(s) | Status |
|---|---|---|---|
| Added room filter empty-state message | Prevents confusion when a selected filter returns no rows | `templates/rooms.html` | Implemented |
| Created development log | Records project iterations and development evidence | `docs/development-log.md` | Implemented |
| Created user guide | Supports staff use and assignment documentation | `docs/user-guide.md` | In progress |
| Created technical notes | Explains system architecture and implementation choices | `docs/technical-notes.md` | In progress |
| Created traceability matrix | Links requirements to implemented features and evidence | `docs/traceability-matrix.md` | In progress |
| Created test results template | Prepares structure for manual testing evidence | `docs/test-results-template.md` | In progress |

---

## Improvements Planned but Not Yet Implemented

| Planned Improvement | Reason | Priority |
|---|---|---|
| Booking filter empty-state message | Keeps booking filtering consistent with room filtering | High |
| Portfolio UI polish | Makes the website more professional and presentation-ready | High |
| Guest editing workflow | Completes guest record management more realistically | Medium |
| Architecture documentation | Supports design explanation and report evidence | Medium |
| Screenshots checklist | Helps collect clear appendix evidence | Medium |

---

## Review Conclusion

The peer review confirmed that the application already meets the core purpose of the project: it provides a working internal system for managing rooms, guests and bookings in a small boutique hotel.

However, the review also identified areas for improvement. The most important next steps are to improve the visual presentation, complete the documentation, collect testing evidence and add one realistic functional improvement such as guest editing.

This feedback will be used in the final evaluation chapter to explain how the project changed during development and how the final system compares with the original requirements.