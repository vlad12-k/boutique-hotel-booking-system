from sqlalchemy import inspect

from hotel_app import create_app
from hotel_app.extensions import db


def test_initial_migration_builds_preserved_schema(tmp_path):
    database_path = tmp_path / "migration.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )

    result = app.test_cli_runner().invoke(args=["db", "upgrade"])
    assert result.exit_code == 0, result.output

    with app.app_context():
        assert set(inspect(db.engine).get_table_names()) == {
            "alembic_version",
            "booking",
            "guest",
            "notification_log",
            "room",
            "security_audit_event",
            "staff_account",
        }
