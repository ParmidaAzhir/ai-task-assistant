
# AI Task Assistant API

Backend AI Engineering Capstone — FlyRank Internship

## Overview

AI Task Assistant is a FastAPI application that helps students organize their tasks, analyze task urgency using AI, and generate PDF reports.

The project demonstrates backend development, database persistence, LLM integration, PDF reporting, and automated testing.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- OpenRouter (LLM integration)
- Pydantic
- ReportLab
- Pytest

## Five Capstone Concepts

| Concept | Implementation |
|---|---|
| API endpoints | `main.py` — task creation, listing, retrieval, analysis, and reports |
| Database | `database.py` — persistent SQLite storage |
| LLM integration | `ai_service.py` — OpenRouter analysis with validated output and token usage |
| PDF reporting | `report_service.py` — downloadable task reports |
| Test suite (swap) | `test_main.py` — automated endpoint and error tests |

### Swap justification

An automated test suite was chosen instead of authentication or background jobs because this small, local, single-user API does not require user accounts or asynchronous processing. Tests help verify that core functionality works reliably.

## Setup

Requires Python 3.10 or newer.

### 1. Clone the repository

```bash
git clone https://github.com/ParmidaAzhir/ai-task-assistant.git
cd ai-task-assistant
```

### 2. Install dependencies

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install packages:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```ini
MOCK_AI=true
OPENROUTER_MODEL=openrouter/free
```

Mock mode works without an API key.

For real AI analysis, add your own OpenRouter API key and change `MOCK_AI=false`.

Never commit your `.env` file.

### 4. Seed demo data

```bash
python seed.py
```

### 5. Start the API

```bash
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs.

## Five-Minute Demo

1. Open `/docs`.
2. Execute `GET /tasks` to see demo tasks.
3. Execute `POST /tasks` to create a task.
4. Execute `POST /tasks/1/analyze` to analyze a task.
5. Execute `GET /reports/tasks` to download the PDF report.

## Run Tests

```bash
python -m pytest -v
```

The tests use an isolated in-memory SQLite database.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{task_id}` | Retrieve a task |
| POST | `/tasks/{task_id}/analyze` | Analyze a task |
| GET | `/reports/tasks` | Download PDF report |

## 10x Goal

Reduce the manual effort of organizing and reviewing study tasks by providing automated AI-assisted task classification and reporting.

This is a project goal, not a measured performance claim.

## Non-Goals

- No frontend application
- No user registration
- No payment processing
- No production deployment

## Security

API keys are loaded from environment variables. The `.gitignore` excludes local secrets, databases, and generated files.

## Author

Parmida Azhir

FlyRank Backend AI Engineering Track
