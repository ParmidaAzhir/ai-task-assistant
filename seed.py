
from database import SessionLocal, Task

demo_tasks = [
    {
        "title": "Study Operating Systems",
        "description": "Review CPU scheduling and process management",
    },
    {
        "title": "Finish AI project",
        "description": "Complete FastAPI backend assignment",
    },
    {
        "title": "Prepare for exam tomorrow",
        "description": "Review university lecture notes",
    },
    {
        "title": "Update GitHub portfolio",
        "description": "Add recent backend projects",
    },
    {
        "title": "Submit internship report",
        "description": "Prepare the final report before the deadline",
    },
]


def seed_database():
    db = SessionLocal()

    try:
        added = 0

        for item in demo_tasks:
            exists = db.query(Task).filter(
                Task.title == item["title"]
            ).first()

            if not exists:
                db.add(Task(**item))
                added += 1

        db.commit()
        print(f"Seed complete: {added} tasks added.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
