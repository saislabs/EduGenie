"""Frontend integration tests for template and static asset delivery."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_index_page_delivery():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text
    assert "EduGenie" in html
    assert "view-dashboard" in html
    assert "view-qa" in html
    assert "view-quiz" in html
    assert "view-explain" in html
    assert "view-summarize" in html
    assert "view-learning" in html


def test_static_css_delivery():
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "--accent-primary" in response.text


def test_static_js_delivery():
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "gemini_ready" in data
