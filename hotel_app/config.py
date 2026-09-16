import os
from collections.abc import Mapping
from typing import Any


DEVELOPMENT_DATABASE_URL = "sqlite:///hotel.db"
UNSAFE_SECRET_VALUES = frozenset({"change-me", "dev", "secret", "your-secret-key"})


def normalise_database_url(value: str) -> str:
    """Return a SQLAlchemy URL using the supported PostgreSQL driver."""
    if value.startswith("postgres://"):
        return value.replace("postgres://", "postgresql+psycopg://", 1)
    if value.startswith("postgresql://"):
        return value.replace("postgresql://", "postgresql+psycopg://", 1)
    return value


class Config:
    APP_ENV = os.getenv("APP_ENV", "development").lower()
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = normalise_database_url(
        os.getenv("DATABASE_URL", DEVELOPMENT_DATABASE_URL)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_ADMIN_TOKEN = os.getenv("API_ADMIN_TOKEN")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = APP_ENV == "production"

    NOTIFICATION_DELIVERY_ENABLED = (
        os.getenv("NOTIFICATION_DELIVERY_ENABLED", "0") == "1"
    )


def validate_config(config: Mapping[str, Any]) -> None:
    """Reject unsafe runtime configuration before serving requests."""
    if config.get("TESTING"):
        return

    secret_key = config.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY must be set in the environment before the application starts."
        )

    if config.get("APP_ENV") != "production":
        return

    if str(secret_key).lower() in UNSAFE_SECRET_VALUES or len(str(secret_key)) < 32:
        raise RuntimeError("Production SECRET_KEY must be at least 32 characters long.")

    database_url = str(config.get("SQLALCHEMY_DATABASE_URI", ""))
    if not database_url.startswith("postgresql+psycopg://"):
        raise RuntimeError("Production requires PostgreSQL through the psycopg driver.")

    if not config.get("SESSION_COOKIE_SECURE"):
        raise RuntimeError("Production sessions require secure cookies.")

    if config.get("NOTIFICATION_DELIVERY_ENABLED"):
        raise RuntimeError(
            "Prototype notification delivery cannot be enabled in production."
        )
