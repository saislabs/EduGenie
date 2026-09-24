"""Unit and integration tests for Personalized Learning Path module."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_learning_path_success():
    payload = {
        "topic": "SQL",
        "current_level": "beginner",
        "available_time": "1 hour/day",
        "goal": "Become interview-ready",
    }
    response = client.post("/api/learn/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res_data = data["data"]
    assert res_data["topic"] == "SQL"
    assert res_data["current_level"] == "beginner"
    assert isinstance(res_data["stages"], list)
    assert len(res_data["stages"]) >= 3

    first_stage = res_data["stages"][0]
    assert "level_number" in first_stage
    assert "level_title" in first_stage
    assert "estimated_time" in first_stage
    assert isinstance(first_stage["topics"], list)
    assert len(first_stage["topics"]) > 0


def test_generate_learning_path_empty_topic():
    payload = {
        "topic": "   ",
        "current_level": "beginner",
    }
    response = client.post("/api/learn/recommendations", json=payload)
    assert response.status_code == 422
    assert response.json()["success"] is False


def test_legacy_learning_route():
    payload = {
        "topic": "Python",
        "current_level": "beginner",
        "available_time": "1 hour/day",
        "goal": "Build web apps",
    }
    response = client.post("/learn/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "stages" in data["data"]
