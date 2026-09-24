from pathlib import Path

from fastapi.testclient import TestClient

from percentile.web import app


def test_web_training_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("PERCENTILE_DB", str(tmp_path / "test.db"))
    client = TestClient(app)

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["ok"] is True

    session = client.get("/api/session?mode=foundation&limit=2")
    assert session.status_code == 200
    questions = session.json()["questions"]
    assert len(questions) == 2
    assert "correct_index" not in questions[0]

    first = questions[0]
    attempt = client.post(
        "/api/attempt",
        json={
            "question_id": first["id"],
            "selected_index": 2,
            "response_seconds": 35,
            "confidence": 0.8,
        },
    )
    assert attempt.status_code == 200
    assert "skeleton" in attempt.json()

    dashboard = client.get("/api/dashboard").json()
    assert dashboard["summary"]["attempts"] == 1


def test_mock_log(tmp_path, monkeypatch):
    monkeypatch.setenv("PERCENTILE_DB", str(tmp_path / "mock.db"))
    client = TestClient(app)

    response = client.post(
        "/api/mock",
        json={
            "name": "Official Practice Exam 1",
            "total_score": 605,
            "quant_score": 75,
            "verbal_score": 82,
            "di_score": 78,
        },
    )
    assert response.status_code == 200

    latest = client.get("/api/dashboard").json()["latest_mock"]
    assert latest["name"] == "Official Practice Exam 1"
    assert latest["total_score"] == 605


def test_recognition_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("PERCENTILE_DB", str(tmp_path / "recognition.db"))
    client = TestClient(app)

    session = client.get("/api/session?mode=recognition&limit=1").json()
    question = session["questions"][0]
    assert "archetype_choices" in question
    assert "correct_index" not in question

    correct_choice = next(
        choice for choice in question["archetype_choices"]
        if choice["id"] == "Q_ALG_LINEAR"
    )
    response = client.post(
        "/api/recognition-attempt",
        json={
            "question_id": question["id"],
            "selected_archetype_id": correct_choice["id"],
            "response_seconds": 8,
            "confidence": 0.9,
        },
    )
    assert response.status_code == 200
    assert response.json()["correct"] is True
    assert "skeleton" in response.json()

    dashboard = client.get("/api/dashboard").json()
    assert dashboard["recognition"]["attempts"] == 1
