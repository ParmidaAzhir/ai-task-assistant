# My 10x Solution — Parmida Azhir

**Project:** AI Task Assistant API  
**Track:** FlyRank Backend AI Engineering  
**Technology:** Python, FastAPI, SQLite, OpenRouter, ReportLab, Pytest

## 1. The Problem

Students often manage several academic responsibilities, including exams, assignments, projects, and deadlines. Organizing these tasks manually can be time-consuming, especially when deciding what needs attention first.

My solution addresses this problem by providing a simple backend system that stores student tasks and uses AI to help classify their urgency and purpose.

## 2. My 10x Solution

I developed an AI Task Assistant API that combines task management, AI-powered analysis, and PDF reporting in one application.

The goal is to make reviewing and organizing academic tasks significantly easier by automating parts of the process that would otherwise require manual effort.

The 10x improvement is a design goal rather than a measured performance result.

## 3. How I Implemented It

The application is built with Python and FastAPI.

Users can create tasks through HTTP endpoints. The application saves the tasks in a SQLite database using SQLAlchemy, allowing information to persist between restarts.

An AI analysis endpoint sends task information to a language model through OpenRouter. The model classifies tasks by category and urgency and provides a short explanation. Pydantic validates the returned data, and the application records token usage.

The system also generates downloadable PDF reports containing saved tasks and their completion status.

Automated tests verify core API operations and reporting functionality.

## 4. Five Backend Concepts

| Concept | Implementation |
|---|---|
| API endpoints | `main.py` — FastAPI endpoints and HTTP responses |
| Database | `database.py` — persistent SQLite storage |
| LLM integration | `ai_service.py` — AI analysis, validation, and token tracking |
| Reporting | `report_service.py` — PDF generation |
| Test suite (swap) | `test_main.py` — automated API tests |

**Swap justification:** I selected automated testing instead of authentication or background jobs because this project is a small, single-user API without account management or long-running processing. Automated tests provide a practical way to verify its reliability.

## 5. How to Run the Project

1. Clone the public GitHub repository.
2. Create and activate a Python virtual environment.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Create a `.env` file using `.env.example` as a template.
5. Run `python seed.py` to populate the database with example tasks.
6. Start the API using `python -m uvicorn main:app --reload`.
7. Open `http://127.0.0.1:8000/docs` to test the endpoints.

The application supports a free mock-analysis mode for testing without an API key. Real AI analysis can be enabled with an OpenRouter key and a compatible model.

## 6. Scope and Limitations

The project intentionally focuses on backend functionality rather than frontend design. It does not include user authentication, payment functionality, or cloud deployment.

It was developed using free tools and locally hosted services, with an optional external AI integration.

## 7. Conclusion

This capstone combines the backend skills I learned throughout the FlyRank internship into a working application. It demonstrates API development, database persistence, AI integration, PDF generation, and automated testing.

The result is a small, reproducible backend project that can be extended with additional features in the future.