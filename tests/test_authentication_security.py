import re

import pytest

import hotel_app.routes as routes_module
from hotel_app import create_app
from hotel_app.extensions import db
from hotel_app.models import Room, SecurityAuditEvent, StaffAccount


CSRF_PATTERN = re.compile(r'name="csrf_token" value="([^"]+)"')
OWNER_EMAIL = "owner@example.com"
OWNER_PASSWORD = "synthetic-owner-passphrase"


def csrf_token(response) -> str:
    match = CSRF_PATTERN.search(response.get_data(as_text=True))
    assert match is not None
    return match.group(1)


def create_owner(application, *, active=True) -> int:
    with application.app_context():
        account = StaffAccount(
            email=OWNER_EMAIL,
            display_name="Synthetic Owner",
            role="owner",
            is_active=active,
        )
        account.set_password(OWNER_PASSWORD)
        db.session.add(account)
        db.session.commit()
        return account.id


def login(client, *, email=OWNER_EMAIL, password=OWNER_PASSWORD, next_url=None):
    path = "/login"
    if next_url:
        path = f"{path}?next={next_url}"
    token = csrf_token(client.get(path))
    return client.post(
        "/login",
        data={
            "csrf_token": token,
            "email": email,
            "password": password,
            "next": next_url or "",
        },
    )


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/rooms",
        "/rooms/add",
        "/guests",
        "/guests/add",
        "/bookings",
        "/bookings/add",
        "/notifications",
    ],
)
def test_owner_html_routes_require_authentication(client, path):
    response = client.get(path)
    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"].startswith("/login?next=")


def test_health_is_public_but_notification_api_is_not(application, client):
    application.config["API_ADMIN_TOKEN"] = "synthetic-api-token"

    assert client.get("/api/health").status_code == 200
    assert client.get("/api/notifications").status_code == 401


def test_successful_login_rotates_session_and_records_audit(application, client):
    account_id = create_owner(application)
    with client.session_transaction() as session_data:
        session_data["pre_auth_marker"] = "must-be-removed"

    response = login(client)

    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"] == "/"
    with client.session_transaction() as session_data:
        assert "pre_auth_marker" not in session_data
        assert session_data["_user_id"] == str(account_id)
        assert session_data["_fresh"] is True

    with application.app_context():
        account = db.session.get(StaffAccount, account_id)
        assert account.last_login_at is not None
        event = SecurityAuditEvent.query.one()
        assert event.event_type == "login_succeeded"
        assert event.outcome == "success"


def test_failed_login_uses_generic_message_and_records_minimal_event(
    application,
    client,
):
    create_owner(application)

    response = login(client, email="unknown@example.com", password="wrong-password")

    assert response.status_code == 401
    assert "Invalid email or password." in response.get_data(as_text=True)
    assert "unknown@example.com" not in response.get_data(as_text=True)
    with application.app_context():
        event = SecurityAuditEvent.query.one()
        assert event.event_type == "login_failed"
        assert event.staff_account_id is None


def test_oversized_password_is_rejected_without_using_account_hash(
    application,
    client,
    monkeypatch,
):
    create_owner(application)
    with application.app_context():
        account_hash = StaffAccount.query.one().password_hash
    checked_hashes = []

    def tracked_check(password_hash, password):
        checked_hashes.append(password_hash)
        return False

    monkeypatch.setattr("hotel_app.auth.check_password_hash", tracked_check)

    response = login(client, password="x" * 129)

    assert response.status_code == 401
    assert len(checked_hashes) == 1
    assert checked_hashes[0] != account_hash


@pytest.mark.parametrize(
    "unsafe_next",
    [
        "https://attacker.example/collect",
        "//attacker.example/collect",
        "/\\attacker.example/collect",
    ],
)
def test_login_rejects_open_redirects(application, client, unsafe_next):
    create_owner(application)

    response = login(client, next_url=unsafe_next)

    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"] == "/"


def test_login_accepts_safe_local_redirect(application, client):
    create_owner(application)

    response = login(client, next_url="/rooms")

    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"] == "/rooms"


def test_logout_requires_csrf_and_clears_authenticated_session(application, client):
    account_id = create_owner(application)
    assert login(client).status_code == 302

    assert client.post("/logout").status_code == 400

    page = client.get("/")
    assert page.status_code == 200
    token = csrf_token(page)
    with client.session_transaction() as session_data:
        assert "csrf_token" in session_data, dict(session_data)
    response = client.post("/logout", data={"csrf_token": token})

    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"] == "/login"
    assert client.get("/").status_code == 302
    with application.app_context():
        events = SecurityAuditEvent.query.order_by(SecurityAuditEvent.id).all()
        assert [(event.event_type, event.staff_account_id) for event in events] == [
            ("login_succeeded", account_id),
            ("logout", account_id),
        ]


def test_state_changing_owner_form_requires_csrf(application, client):
    create_owner(application)
    assert login(client).status_code == 302

    response = client.post(
        "/rooms/add",
        data={
            "room_number": "S-1",
            "room_type": "Synthetic",
            "price_per_night": "100",
            "status": "Available",
        },
    )

    assert response.status_code == 400
    with application.app_context():
        assert Room.query.count() == 0


def test_valid_csrf_preserves_room_workflow(application, client):
    create_owner(application)
    assert login(client).status_code == 302
    page = client.get("/rooms/add")
    assert page.status_code == 200
    token = csrf_token(page)
    with client.session_transaction() as session_data:
        assert "csrf_token" in session_data, dict(session_data)

    response = client.post(
        "/rooms/add",
        data={
            "csrf_token": token,
            "room_number": "S-1",
            "room_type": "Synthetic",
            "price_per_night": "100",
            "status": "Available",
        },
    )

    assert response.status_code == 302, response.get_data(as_text=True)
    with application.app_context():
        assert Room.query.filter_by(room_number="S-1").one()


def test_login_rate_limit_blocks_repeated_attempts(application, client):
    application.config["LOGIN_RATE_LIMIT"] = "2 per minute"

    first = login(client, email="rate-limit@example.com", password="wrong")
    second = login(client, email="rate-limit@example.com", password="wrong")
    third = login(client, email="rate-limit@example.com", password="wrong")

    assert (first.status_code, second.status_code, third.status_code) == (
        401,
        401,
        429,
    )


def test_login_ip_rate_limit_blocks_email_rotation(application, client):
    application.config.update(
        LOGIN_RATE_LIMIT="10 per minute",
        LOGIN_IP_RATE_LIMIT="2 per minute",
    )

    first = login(client, email="first@example.com", password="wrong")
    second = login(client, email="second@example.com", password="wrong")
    third = login(client, email="third@example.com", password="wrong")

    assert (first.status_code, second.status_code, third.status_code) == (
        401,
        401,
        429,
    )


def test_notification_api_uses_constant_time_token_comparison(
    application,
    client,
    monkeypatch,
):
    application.config["API_ADMIN_TOKEN"] = "synthetic-api-token"
    compared = []

    def tracked_compare(expected, provided):
        compared.append((expected, provided))
        return expected == provided

    monkeypatch.setattr(routes_module.secrets, "compare_digest", tracked_compare)

    response = client.get(
        "/api/notifications",
        headers={"X-API-Key": "synthetic-api-token"},
    )

    assert response.status_code == 200
    assert compared == [("synthetic-api-token", "synthetic-api-token")]


def test_notification_api_rate_limit(application, client):
    application.config.update(
        API_ADMIN_TOKEN="synthetic-api-token",
        API_RATE_LIMIT="2 per minute",
    )
    headers = {"X-API-Key": "synthetic-api-token"}

    assert client.get("/api/notifications", headers=headers).status_code == 200
    assert client.get("/api/notifications", headers=headers).status_code == 200
    assert client.get("/api/notifications", headers=headers).status_code == 429


def test_security_headers_are_applied(client):
    response = client.get("/api/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["Cache-Control"] == "no-store"
    assert "Strict-Transport-Security" not in response.headers


def test_production_health_adds_hsts():
    app = create_app(
        {
            "TESTING": True,
            "APP_ENV": "production",
            "SECRET_KEY": "synthetic-production-secret-key-32-characters",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SESSION_COOKIE_SECURE": True,
            "REMEMBER_COOKIE_SECURE": True,
        }
    )

    response = app.test_client().get("/api/health")
    assert response.headers["Strict-Transport-Security"].startswith("max-age=")


def test_secure_session_cookie_configuration_is_emitted():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-cookie-test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SESSION_COOKIE_SECURE": True,
            "REMEMBER_COOKIE_SECURE": True,
        }
    )

    response = app.test_client().get(
        "/login",
        base_url="https://localhost",
    )
    cookie = response.headers["Set-Cookie"]

    assert "haifa_ops_session=" in cookie
    assert "Secure" in cookie
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie
    assert app.config["SESSION_REFRESH_EACH_REQUEST"] is False


def test_bootstrap_owner_hashes_password_and_is_single_use(
    application,
    monkeypatch,
):
    monkeypatch.setenv("BOOTSTRAP_OWNER_EMAIL", "OWNER@EXAMPLE.COM")
    monkeypatch.setenv("BOOTSTRAP_OWNER_NAME", "Synthetic Owner")
    monkeypatch.setenv("BOOTSTRAP_OWNER_PASSWORD", OWNER_PASSWORD)
    runner = application.test_cli_runner()

    result = runner.invoke(args=["bootstrap-owner"])

    assert result.exit_code == 0, result.output
    assert result.output == "Initial owner account created.\n"
    with application.app_context():
        account = StaffAccount.query.one()
        assert account.email == OWNER_EMAIL
        assert account.role == "owner"
        assert account.password_hash.startswith("scrypt:")
        assert OWNER_PASSWORD not in account.password_hash
        assert account.check_password(OWNER_PASSWORD)
        event = SecurityAuditEvent.query.one()
        assert event.event_type == "owner_bootstrapped"

    repeated = runner.invoke(args=["bootstrap-owner"])
    assert repeated.exit_code != 0
    assert "already exists" in repeated.output


def test_bootstrap_owner_rejects_weak_password(application, monkeypatch):
    monkeypatch.setenv("BOOTSTRAP_OWNER_EMAIL", OWNER_EMAIL)
    monkeypatch.setenv("BOOTSTRAP_OWNER_NAME", "Synthetic Owner")
    monkeypatch.setenv("BOOTSTRAP_OWNER_PASSWORD", "too-short")

    result = application.test_cli_runner().invoke(args=["bootstrap-owner"])

    assert result.exit_code != 0
    assert "at least 14 characters" in result.output
    with application.app_context():
        assert StaffAccount.query.count() == 0
