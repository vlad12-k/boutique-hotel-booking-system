import click
from flask import Flask

from hotel_app.extensions import db
from hotel_app.models import Room


ACADEMIC_DEMO_ROOMS = (
    ("101", "Single", 70.0),
    ("102", "Single", 70.0),
    ("103", "Double", 95.0),
    ("104", "Double", 95.0),
    ("105", "Twin", 90.0),
    ("106", "Twin", 90.0),
    ("107", "Deluxe", 130.0),
    ("108", "Deluxe", 130.0),
    ("109", "Suite", 180.0),
    ("110", "Suite", 180.0),
)


def register_cli(app: Flask) -> None:
    @app.cli.command("seed-academic-demo")
    def seed_academic_demo() -> None:
        """Seed the original synthetic ten-room academic dataset explicitly."""
        if Room.query.count() > 0:
            raise click.ClickException("Room inventory is not empty; seed aborted.")

        db.session.add_all(
            Room(
                room_number=number,
                room_type=room_type,
                price_per_night=price,
                status="Available",
            )
            for number, room_type, price in ACADEMIC_DEMO_ROOMS
        )
        db.session.commit()
        click.echo("Academic demo rooms created.")
