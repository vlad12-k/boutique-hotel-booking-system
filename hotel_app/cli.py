import os
from decimal import Decimal

import click
from flask import Flask
from sqlalchemy.exc import IntegrityError

from hotel_app.extensions import db
from hotel_app.inventory import (
    HAIFA_ROOMS,
    HAIFA_ROOM_TYPES,
    configured_room_type_values,
)
from hotel_app.models import Room, RoomType, SecurityAuditEvent, StaffAccount
from hotel_app.security import is_valid_email, normalise_email, validate_new_password


ACADEMIC_DEMO_ROOMS = (
    ("101", "Single", Decimal("70.00")),
    ("102", "Single", Decimal("70.00")),
    ("103", "Double", Decimal("95.00")),
    ("104", "Double", Decimal("95.00")),
    ("105", "Twin", Decimal("90.00")),
    ("106", "Twin", Decimal("90.00")),
    ("107", "Deluxe", Decimal("130.00")),
    ("108", "Deluxe", Decimal("130.00")),
    ("109", "Suite", Decimal("180.00")),
    ("110", "Suite", Decimal("180.00")),
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

        room_types = {}
        for label in {item[1] for item in ACADEMIC_DEMO_ROOMS}:
            room_type = RoomType(
                code=f"academic-{label.lower()}",
                display_name=label,
                bathroom_type="unspecified",
            )
            db.session.add(room_type)
            room_types[label] = room_type

        for number, label, price in ACADEMIC_DEMO_ROOMS:
            db.session.add(
                Room(
                    room_number=number,
                    room_type=room_types[label],
                    price_per_night=price,
                    currency="GBP",
                    operational_state="ready",
                )
            )
        db.session.commit()
        click.echo("Academic demo rooms created.")

    @app.cli.command("seed-haifa-inventory")
    def seed_haifa_inventory() -> None:
        """Create the configurable seven-room production inventory."""
        if Room.query.count() > 0 or RoomType.query.count() > 0:
            raise click.ClickException("Room inventory is not empty; seed aborted.")

        room_types = {}
        try:
            for contract in HAIFA_ROOM_TYPES:
                label, rate = configured_room_type_values(app.config, contract)
                room_type = RoomType(
                    code=contract.code,
                    display_name=label,
                    bathroom_type=contract.bathroom_type,
                    has_balcony_or_terrace=contract.has_balcony_or_terrace,
                )
                db.session.add(room_type)
                room_types[contract.code] = (room_type, rate)
        except ValueError as error:
            db.session.rollback()
            raise click.ClickException(str(error)) from error

        for contract in HAIFA_ROOMS:
            room_type, rate = room_types[contract.room_type_code]
            db.session.add(
                Room(
                    room_number=contract.number,
                    room_type=room_type,
                    price_per_night=rate.amount,
                    currency=rate.currency,
                    operational_state="ready",
                )
            )

        db.session.commit()
        click.echo("Haifa Guest House seven-room inventory created.")
