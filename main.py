
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ai_service import analyze_task
from fastapi.responses import StreamingResponse
from report_service import generate_task_report

from database import SessionLocal, Task

app = FastAPI(title="AI Task Assistant API")


class TaskCreate(BaseModel):
    title: str
    description: str = ""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "AI Task Assistant API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed": new_task.completed
    }


@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
        for task in tasks
    ]


@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

@app.post("/tasks/{task_id}/analyze")
def analyze_existing_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    analysis = analyze_task(
        task.title,
        task.description or ""
    )

    return {
        "task_id": task.id,
        "title": task.title,
        "analysis": analysis
    }


@app.get("/reports/tasks")
def download_task_report(db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.id).all()
    pdf = generate_task_report(tasks)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=task-report.pdf"
        }
    )
