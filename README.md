# Boutique Hotel Booking and Room Management System

## Project Purpose
This project is an academic prototype for Unit 36: Application Development. It provides a simple staff-facing application for managing guests, rooms, bookings, room availability and check-in/check-out workflow for a boutique hotel with 10 rooms.

## Technology Stack
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2 templates
- Bootstrap
- Vanilla JavaScript (client-side validation, filtering and interaction)

## Setup Instructions
1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the App
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

Optional environment variables:
- `SECRET_KEY` (recommended outside local prototype use so sessions stay stable)
- `FLASK_DEBUG=1` (local development only)

## Implemented Features
- Dashboard with room counts, today's check-ins/check-outs and recent bookings
- Room management: list, add and update room status
- Initial seed of 10 boutique hotel rooms
- Guest management: list and add guests with contact details
- Booking management: list, create, cancel, check-in and check-out bookings
- Validation for required fields, date logic, maintenance-room booking restrictions and overlapping active bookings
- Check-in/check-out workflow that updates both booking status and room status

## Academic Note
This is an academic MVP prototype for a small 10-room boutique hotel and is designed to be simple, understandable and easy to demonstrate in coursework.
Vanilla JavaScript is used for client-side validation, filtering and user interaction, while Flask handles backend logic and database persistence.

## Future Improvements
- Role-based login and permissions
- PostgreSQL migration
- Cloud deployment
- Automated backups
- Email confirmations
- Online payment integration
