"""Unit and integration tests for History & Progress modules."""

import pytest
from fastapi.testclient import TestClient
from main import app
from services.storage_service import storage

client = TestClient(app)


def test_history_and_progress_integration():
    # 1. Post a Q&A request to populate database
    qa_payload = {
        "question": "What is Object-Oriented Programming?",
        "context": "Software Engineering",
    }
    qa_res = client.post("/api/qa", json=qa_payload)
    assert qa_res.status_code == 200

    # 2. Verify history endpoint contains the item
    hist_res = client.get("/api/history?activity_type=qa")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()["data"]
    assert len(hist_data) >= 1
    recent_id = hist_data[0]["id"]

    # 3. Retrieve single item
    item_res = client.get(f"/api/history/{recent_id}")
    assert item_res.status_code == 200
    assert item_res.json()["data"]["id"] == recent_id

    # 4. Check progress metrics endpoint
    prog_res = client.get("/api/progress")
    assert prog_res.status_code == 200
    prog_data = prog_res.json()["data"]
    assert prog_data["questions_asked"] >= 1
    assert prog_data["total_activities"] >= 1

    # 5. Delete the item
    del_res = client.delete(f"/api/history/{recent_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # 6. Verify 404 on deleted item
    not_found_res = client.get(f"/api/history/{recent_id}")
    assert not_found_res.status_code == 404
