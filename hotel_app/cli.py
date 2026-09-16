import os

import click
from flask import Flask
from sqlalchemy.exc import IntegrityError

from hotel_app.extensions import db
from hotel_app.models import Room, SecurityAuditEvent, StaffAccount
from hotel_app.security import is_valid_email, normalise_email, validate_new_password


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
    @app.cli.command("bootstrap-owner")
    def bootstrap_owner() -> None:
        """Create the first owner account without command-line credentials."""
        if StaffAccount.query.count() > 0:
            raise click.ClickException(
                "A staff account already exists; owner bootstrap aborted."
            )

        email = normalise_email(
            os.getenv("BOOTSTRAP_OWNER_EMAIL")
            or click.prompt("Owner email", type=str)
        )
        display_name = (
            os.getenv("BOOTSTRAP_OWNER_NAME")
            or click.prompt("Owner display name", type=str)
        ).strip()
        password = os.getenv("BOOTSTRAP_OWNER_PASSWORD") or click.prompt(
            "Owner password",
            hide_input=True,
            confirmation_prompt=True,
        )

        if not is_valid_email(email):
            raise click.ClickException("A valid owner email is required.")
        if not display_name or len(display_name) > 120:
            raise click.ClickException(
                "Owner display name must contain between 1 and 120 characters."
            )

        try:
            validate_new_password(password)
        except ValueError as error:
            raise click.ClickException(str(error)) from error

        account = StaffAccount(
            email=email,
            display_name=display_name,
            role="owner",
            is_active=True,
        )
        account.set_password(password)
        db.session.add(account)

        try:
            db.session.flush()
            db.session.add(
                SecurityAuditEvent(
                    staff_account_id=account.id,
                    event_type="owner_bootstrapped",
                    outcome="success",
                )
            )
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise click.ClickException(
                "Owner bootstrap could not be completed."
            ) from error

        click.echo("Initial owner account created.")

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
