"""Unit and integration tests for Concept Explanation module."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_explain_concept_success():
    payload = {
        "concept": "Neural Networks",
        "difficulty": "intermediate",
        "style": "step_by_step",
    }
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res_data = data["data"]
    assert res_data["concept"] != ""
    assert res_data["difficulty"] == "intermediate"
    assert "simple_explanation" in res_data
    assert "how_it_works" in res_data
    assert "example" in res_data
    assert isinstance(res_data["key_points"], list)


def test_explain_concept_empty_fails():
    payload = {"concept": " "}
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False


def test_explain_concept_fallback_difficulty():
    payload = {
        "concept": "Binary Search",
        "difficulty": "unknown_difficulty_string",
        "style": "unknown_style_string",
    }
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Sanitized to defaults
    assert data["data"]["difficulty"] == "intermediate"
    assert data["data"]["style"] == "simple"


def test_legacy_explain_route():
    payload = {
        "concept": "Recursion",
        "difficulty": "beginner",
        "style": "simple",
    }
    response = client.post("/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "simple_explanation" in data["data"]
