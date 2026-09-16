import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from hotel_app import create_app
from hotel_app.extensions import db


@pytest.fixture()
def application(tmp_path):
    database_path = tmp_path / "application_test.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "API_ADMIN_TOKEN": None,
        }
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(application):
    return application.test_client()
