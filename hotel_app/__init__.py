from collections.abc import Mapping
from typing import Any

from dotenv import load_dotenv
from flask import Flask

from hotel_app.auth import auth as auth_blueprint
from hotel_app.cli import register_cli
from hotel_app.config import Config, validate_config
from hotel_app.extensions import csrf, db, limiter, login_manager, migrate
from hotel_app.routes import register_routes
from hotel_app.security import register_security_headers


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
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to continue."
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"

    app.register_blueprint(auth_blueprint)
    register_routes(app)
    register_cli(app)
    register_security_headers(app)
    return app
