
import os

os.environ["MOCK_AI"] = "true"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_read_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Testing the API"
        }
    )

    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test task"


def test_missing_task():
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_ai_analysis():
    response = client.post(
        "/tasks",
        json={
            "title": "Study for exam tomorrow",
            "description": "Review Operating Systems"
        }
    )

    task_id = response.json()["id"]
    response = client.post(f"/tasks/{task_id}/analyze")

    assert response.status_code == 200
    assert response.json()["analysis"]["urgency"] == "high"


def test_pdf_report():
    response = client.get("/reports/tasks")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
