"""Unit and integration tests for Quiz Generator module."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_and_evaluate_quiz():
    # 1. Generate Quiz
    gen_payload = {
        "topic": "Machine Learning",
        "num_questions": 3,
        "difficulty": "intermediate",
    }
    gen_res = client.post("/api/quiz", json=gen_payload)
    assert gen_res.status_code == 200
    gen_data = gen_res.json()
    assert gen_data["success"] is True
    quiz = gen_data["data"]
    quiz_id = quiz["quiz_id"]
    assert quiz_id != ""
    assert len(quiz["questions"]) > 0

    # Ensure client questions do NOT expose correct_answer or explanation
    first_q = quiz["questions"][0]
    assert "correct_answer" not in first_q
    assert "explanation" not in first_q
    assert len(first_q["options"]) == 4

    # 2. Submit Answers for Evaluation
    answers = {}
    for q in quiz["questions"]:
        # Select first option 'A' for all
        answers[q["id"]] = "A"

    eval_payload = {
        "quiz_id": quiz_id,
        "user_answers": answers,
    }
    eval_res = client.post("/api/quiz/evaluate", json=eval_payload)
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data["success"] is True
    res = eval_data["data"]
    assert res["quiz_id"] == quiz_id
    assert res["total_questions"] == len(quiz["questions"])
    assert res["correct_count"] + res["incorrect_count"] == res["total_questions"]
    assert 0.0 <= res["score_percentage"] <= 100.0
    assert len(res["results"]) == res["total_questions"]
    # Explanations must be present in evaluation result
    assert "explanation" in res["results"][0]


def test_generate_quiz_empty_topic():
    payload = {"topic": " "}
    response = client.post("/api/quiz", json=payload)
    assert response.status_code == 422
    assert response.json()["success"] is False


def test_evaluate_nonexistent_quiz():
    payload = {
        "quiz_id": "non-existent-uuid-12345",
        "user_answers": {1: "A"},
    }
    response = client.post("/api/quiz/evaluate", json=payload)
    assert response.status_code == 404


def test_legacy_quiz_route():
    payload = {
        "topic": "Operating Systems",
        "num_questions": 3,
        "difficulty": "beginner",
    }
    response = client.post("/quiz", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "quiz_id" in data["data"]
