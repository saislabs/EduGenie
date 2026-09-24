"""Unit and integration tests for Summarization module."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_summarize_content_success():
    sample_text = (
        "Operating systems provide an abstraction layer between computer hardware and user applications. "
        "Key functions include process management, memory allocation, storage access, and device drivers. "
        "Virtual memory allows programs to address more memory than is physically installed by swapping "
        "inactive pages to disk storage. Modern operating systems implement preemptive multitasking."
    )
    payload = {
        "content": sample_text,
        "length": "short",
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res_data = data["data"]
    assert "summary" in res_data
    assert len(res_data["summary"]) > 10
    assert isinstance(res_data["key_points"], list)
    assert isinstance(res_data["important_terms"], list)
    assert isinstance(res_data["quick_revision"], list)


def test_summarize_too_short():
    payload = {
        "content": "Short text.",
        "length": "medium",
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 422
    assert response.json()["success"] is False


def test_legacy_summarize_route():
    sample_text = (
        "Operating systems provide an abstraction layer between computer hardware and user applications. "
        "Key functions include process management, memory allocation, storage access, and device drivers."
    )
    payload = {
        "content": sample_text,
        "length": "medium",
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "summary" in data["data"]
