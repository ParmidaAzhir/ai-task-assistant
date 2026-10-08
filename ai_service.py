
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def analyze_task(title: str, description: str = ""):
    # Free development mode
    if os.getenv("MOCK_AI", "true").lower() == "true":
        text = f"{title} {description}".lower()

        if any(word in text for word in ["exam", "urgent", "deadline", "tomorrow"]):
            urgency = "high"
        elif any(word in text for word in ["study", "review", "project"]):
            urgency = "normal"
        else:
            urgency = "low"

        category = "study" if any(
            word in text for word in ["study", "exam", "review", "university"]
        ) else "other"

        return {
            "category": category,
            "urgency": urgency,
            "reason": "Mock analysis based on task keywords",
            "mode": "mock"
        }

    # Real LLM mode
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze the user's task. Return only a JSON object "
                    "with category (study, work, personal, other), "
                    "urgency (low, normal, high), and reason."
                )
            },
            {
                "role": "user",
                "content": json.dumps({
                    "title": title,
                    "description": description
                })
            }
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    result["mode"] = "live"
    return result
