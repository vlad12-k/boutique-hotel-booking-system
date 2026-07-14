from app import app


def test_api_health_endpoint_returns_service_status():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "boutique-hotel-booking-system"
    assert "housekeeping-notifications" in data["features"]
    assert "notification-logging" in data["features"]


def test_api_notifications_endpoint_requires_api_key(monkeypatch):
    monkeypatch.setenv("API_ADMIN_TOKEN", "test-admin-token")
    client = app.test_client()

    response = client.get("/api/notifications")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorised"}


def test_api_notifications_endpoint_returns_list_with_valid_api_key(monkeypatch):
    monkeypatch.setenv("API_ADMIN_TOKEN", "test-admin-token")
    client = app.test_client()

    response = client.get(
        "/api/notifications",
        headers={"X-API-Key": "test-admin-token"},
    )

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)