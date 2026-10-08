
import os

os.environ["MOCK_AI"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_read_task(client):
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


def test_missing_task(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404


def test_ai_analysis(client):
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


def test_pdf_report(client):
    response = client.get("/reports/tasks")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
