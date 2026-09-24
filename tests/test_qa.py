"""Unit and integration tests for Q&A module."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ask_question_success():
    payload = {
        "question": "What is Artificial Intelligence?",
        "context": "Computer Science",
    }
    response = client.post("/api/qa", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    res_data = data["data"]
    assert "answer" in res_data
    assert "simple_explanation" in res_data
    assert isinstance(res_data["key_points"], list)
    assert len(res_data["key_points"]) > 0


def test_ask_question_empty_fails():
    payload = {"question": "   "}
    response = client.post("/api/qa", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False


def test_ask_question_too_short():
    payload = {"question": "A"}
    response = client.post("/api/qa", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False


def test_legacy_qa_route():
    payload = {
        "question": "What is Python?",
        "context": "Programming",
    }
    response = client.post("/qa", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer" in data["data"]
