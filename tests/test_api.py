import sqlite3

import pytest
from fastapi.testclient import TestClient
from app.main import create_app

def make_client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    return TestClient(app)

def test_health_check(tmp_path):
    client = make_client(tmp_path)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_url_and_persist(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/api/urls", json={"url": "https://example.com/path"})
    assert response.status_code == 201
    body = response.json()
    assert body["shortCode"]
    assert body["originalUrl"] == "https://example.com/path"
    assert body["shortUrl"].endswith("/r/" + body["shortCode"])
    analytics = client.get(f"/api/urls/{body['shortCode']}/analytics")
    assert analytics.status_code == 200
    assert analytics.json()["clickCount"] == 0

def test_invalid_url_rejected(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/api/urls", json={"url": "not-a-url"})
    assert response.status_code == 422


def test_non_unique_integrity_error_is_not_swallowed(tmp_path, monkeypatch):
    client = make_client(tmp_path)

    class FailingConnection:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def execute(self, *args, **kwargs):
            raise sqlite3.IntegrityError("FOREIGN KEY constraint failed")

    monkeypatch.setattr("app.main.connect", lambda db_path: FailingConnection())

    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        client.post("/api/urls", json={"url": "https://example.com"})


def test_unsupported_scheme_rejected(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/api/urls", json={"url": "ftp://example.com/file"})
    assert response.status_code == 422

def test_redirect_and_click_count(tmp_path):
    client = make_client(tmp_path)
    created = client.post("/api/urls", json={"url": "https://example.com"}).json()
    response = client.get(f"/r/{created['shortCode']}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/"
    analytics = client.get(f"/api/urls/{created['shortCode']}/analytics").json()
    assert analytics["clickCount"] == 1
    assert analytics["lastAccessedAtUtc"] is not None

def test_unknown_code_returns_404(tmp_path):
    client = make_client(tmp_path)
    response = client.get("/r/doesnotexist", follow_redirects=False)
    assert response.status_code == 404

def test_unknown_analytics_returns_404(tmp_path):
    client = make_client(tmp_path)
    response = client.get("/api/urls/missing/analytics")
    assert response.status_code == 404

def test_requirement_analysis_greenfield(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/api/requirements/analyze", json={
        "requirement": "Build a scalable URL shortener service with APIs, persistence, and analytics.",
        "scenario_type": "greenfield"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["scenario_type"] == "greenfield"
    assert len(body["tasks"]) >= 3
    assert body["validation_checks"]
    assert body["risks"]

def test_requirement_analysis_brownfield(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/api/requirements/analyze", json={
        "requirement": "Enhance the existing URL service to support click analytics.",
        "scenario_type": "brownfield"
    })
    assert response.status_code == 200
    assert response.json()["scenario_type"] == "brownfield"

def test_requirement_analysis_ambiguous(tmp_path):
    client = make_client(tmp_path)
    response = client.post("/api/requirements/analyze", json={
        "requirement": "Make our service better for customers.",
        "scenario_type": "ambiguous"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["ambiguities"]
    assert "clarification" in body["tasks"][1]["task"].lower() or "ambiguities" in body["tasks"][1]["task"].lower()
