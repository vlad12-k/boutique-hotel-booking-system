# Peer Review Record and Response

## Project

Boutique Hotel Booking and Room Management System

## Module

Application Development

## Author

Vladyslav Kononov

## Review Details

| Field | Information |
|---|---|
| Review source | Application Development Lecturer |
| Review date | 22 June 2026 |
| Reviewed material | Software Design Document |
| Review type | Model peer review supplied for use in place of peer feedback |

---

## Purpose

This document records the model peer review supplied by the Application Development lecturer for use in place of peer feedback.

The project was completed individually, and I was the only student in the group. The lecturer therefore supplied a model review that could be used as the peer-feedback evidence for this stage of the project.

This document records:

- the main feedback received;
- three areas where I agree with the feedback;
- the changes made or planned in response;
- one recommendation not implemented within the current MVP;
- one new development opportunity identified through the review.

The response below represents my own interpretation of the supplied feedback.

---

## Feedback Received

### Strengths Identified

The review identified several strengths in the Software Design Document.

The business problem was considered clear because the document explained how paper records, spreadsheets and separate messages could become inconsistent.

The BP1–BP5 structure was also identified as a strength because each business problem was connected to an appropriate system response.

The Agile methodology section was considered one of the strongest parts of the document because it:

- justified the use of Agile for individual development completed in stages;
- explained why an iterative process was appropriate;
- explained why Waterfall was not selected.

The original user requirements, UR1–UR7, were also considered clear and relevant to the boutique hotel scenario.

---

## Recommended Improvements

### 1. Add graphical design diagrams

The review identified the absence of graphical design artefacts as the main weakness.

The original database structure was presented mainly through a table, while workflows were described using written arrows.

The recommended diagrams were:

- an Entity Relationship Diagram showing the relationships between Guest, Booking and Room;
- a Data Flow Diagram showing how information moves through the application.

### 2. Improve the non-functional requirements

The review identified that most of the original system requirements were functional.

It recommended adding clearer non-functional requirements covering areas such as:

- security;
- usability;
- reliability.

The review also recommended replacing subjective wording, such as “simple enough for non-technical users”, with wording that could be assessed more objectively.

### 3. Improve the risk assessment and assumptions

The original risk table included impact and mitigation but did not include likelihood.

The review recommended adding a likelihood rating so that the most urgent risks could be identified and prioritised.

It also recommended stating the main project assumptions explicitly, particularly:

- the hotel initially has 10 rooms;
- the application is intended for local use.

### 4. Consider future development opportunities

The review identified several possible longer-term improvements:

- replacing SQLite with a server-based database if the application is used across several machines;
- introducing role-based logins for reception, housekeeping and management staff;
- adding an availability calendar instead of relying only on room-status fields.

These suggestions were identified as future improvements rather than required MVP functionality.

---

## Where I Agree and What I Changed

### 1. Add visual design evidence

I agree that the original design relied too heavily on written explanations and tables.

I added an Entity Relationship Diagram showing the relationships between:

- Guest;
- Room;
- Booking.

I also expanded the design documentation with:

- a system architecture diagram;
- a booking creation and validation workflow;
- a check-in and check-out workflow;
- room and booking status lifecycle diagrams;
- a dashboard information-flow diagram.

A clearly labelled Data Flow Diagram will also be included in the final design evidence to show how information moves between the staff user, application processes and database.

### 2. Strengthen the non-functional requirements

I agree that the original requirements were mainly functional and that some usability wording was subjective.

I added a separate non-functional requirements section covering:

- usability;
- maintainability;
- reliability;
- portability;
- responsiveness;
- data minimisation;
- testability;
- security.

The wording was also improved so that the requirements can be connected more clearly to implementation and testing evidence.

### 3. Add risk likelihood and state assumptions

I agree that impact and mitigation alone do not show which risks are most urgent.

The main risk table should include a likelihood rating so that risks can be compared and prioritised more clearly.

The following assumptions have also been stated explicitly:

- the hotel initially operates with 10 rooms;
- the system is intended for internal staff use;
- the application is designed for local academic demonstration;
- SQLite is suitable for the current prototype;
- the MVP is not intended to represent a complete production hotel-management platform.

---

## Feedback I Decided Not to Implement Within the Current MVP

I decided not to migrate the application from SQLite to PostgreSQL or another server-based database as part of the current MVP.

The application is a local academic prototype for a small 10-room boutique hotel. SQLite is proportionate to this scope because it:

- requires minimal configuration;
- supports the relational Guest, Room and Booking structure;
- allows the application to run locally;
- is sufficient for demonstrating the required booking and room-management workflows.

A server-based database would be more appropriate if the application were deployed across several machines or used concurrently by multiple authenticated staff members.

The recommendation has therefore not been rejected completely. It has been recorded as a future production improvement.

---

## New Opportunity Identified Through the Review

The review made me consider an availability-calendar view.

The current application uses:

- booking dates;
- room statuses;
- room filtering;
- booking filtering;
- overlap prevention.

These features are appropriate for the current MVP. However, an availability calendar could give staff a clearer visual overview of future hotel activity.

A future calendar could display:

- rooms as rows;
- dates as columns;
- occupied periods;
- expected arrivals;
- expected departures;
- cleaning periods;
- maintenance periods.

This improvement was not included in the current MVP because it would require additional database queries, interface components and frontend interaction logic.

---

## Actions and Evidence

| Feedback Item | Response | Evidence | Status |
|---|---|---|---|
| Add ERD | Added a visual relationship diagram for Guest, Room and Booking | `docs/design-diagrams.md` | Completed |
| Add DFD | Include a clearly labelled Data Flow Diagram | `docs/design-diagrams.md` | In progress |
| Add non-functional requirements | Added a separate non-functional requirements section | `docs/requirements.md` | Completed |
| Make subjective requirements more testable | Revised the requirement wording and linked it to evidence | `docs/requirements.md` | Completed |
| State assumptions | Added the 10-room, local-use and academic-MVP assumptions | `docs/requirements.md` | Completed |
| Add risk likelihood | Add or verify the likelihood column in the main risk table | Application Development report | To be verified |
| Consider server database | Retained as a future production improvement | Project documentation | Deferred |
| Consider role-based access | Retained as a future production improvement | Project documentation | Deferred |
| Consider availability calendar | Recorded as a future development opportunity | Project documentation | Deferred |

---

## Conclusion

The peer review confirmed that the project had a strong foundation:

- a clear business problem;
- relevant user requirements;
- a justified Agile methodology;
- an appropriate MVP scope.

The most important weakness was the lack of visual design evidence.

In response to the review, I added an Entity Relationship Diagram, expanded the design documentation, strengthened the non-functional requirements and stated the project assumptions explicitly.

The risk table will also be checked to ensure that likelihood is included.

I decided not to migrate from SQLite within the current MVP because the additional complexity would not be proportionate to a local 10-room academic prototype.

The review also helped identify an availability calendar as a realistic future improvement that could make future room occupancy easier for hotel staff to understand.