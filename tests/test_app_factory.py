import pytest
from sqlalchemy import inspect

from hotel_app import create_app
from hotel_app.config import normalise_database_url
from hotel_app.extensions import db


def test_factory_does_not_create_or_seed_database(tmp_path):
    database_path = tmp_path / "empty.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )

    with app.app_context():
        assert inspect(db.engine).get_table_names() == []


def test_factory_registers_preserved_health_route(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'health.db'}",
        }
    )

    response = app.test_client().get("/api/health")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("postgres://db.example/app", "postgresql+psycopg://db.example/app"),
        ("postgresql://db.example/app", "postgresql+psycopg://db.example/app"),
        ("sqlite:///hotel.db", "sqlite:///hotel.db"),
    ],
)
def test_database_url_normalisation(source, expected):
    assert normalise_database_url(source) == expected


def test_production_rejects_sqlite():
    with pytest.raises(RuntimeError, match="Production requires PostgreSQL"):
        create_app(
            {
                "APP_ENV": "production",
                "SECRET_KEY": "a-secure-production-key-with-32-characters",
                "SESSION_COOKIE_SECURE": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///unsafe.db",
            }
        )


def test_production_rejects_short_secret():
    with pytest.raises(RuntimeError, match="at least 32 characters"):
        create_app(
            {
                "APP_ENV": "production",
                "SECRET_KEY": "short",
                "SESSION_COOKIE_SECURE": True,
                "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg://db.example/app",
            }
        )


def test_production_rejects_prototype_notification_delivery():
    with pytest.raises(RuntimeError, match="notification delivery"):
        create_app(
            {
                "APP_ENV": "production",
                "SECRET_KEY": "a-secure-production-key-with-32-characters",
                "SESSION_COOKIE_SECURE": True,
                "SQLALCHEMY_DATABASE_URI": (
                    "postgresql+psycopg://db.example/app"
                ),
                "NOTIFICATION_DELIVERY_ENABLED": True,
            }
        )
