from collections.abc import Mapping
from typing import Any

from dotenv import load_dotenv
from flask import Flask

from hotel_app.cli import register_cli
from hotel_app.config import Config, validate_config
from hotel_app.extensions import db, migrate
from hotel_app.routes import register_routes


def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
    """Create an application instance without changing database state."""
    load_dotenv()

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    validate_config(app.config)
    db.init_app(app)
    migrate.init_app(app, db)
    register_routes(app)
    register_cli(app)
    return app
