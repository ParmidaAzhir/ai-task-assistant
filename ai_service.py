
import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class TaskAnalysis(BaseModel):
    category: Literal["study", "work", "personal", "other"]
    urgency: Literal["low", "normal", "high"]
    reason: str = Field(min_length=1, max_length=500)


def analyze_task(title: str, description: str = ""):
    if os.getenv("MOCK_AI", "true").lower() == "true":
        text = f"{title} {description}".lower()

        urgency = (
            "high"
            if any(word in text for word in
                   ["exam", "urgent", "deadline", "tomorrow"])
            else "normal"
        )

        category = (
            "study"
            if any(word in text for word in
                   ["study", "exam", "review", "university"])
            else "other"
        )

        result = TaskAnalysis(
            category=category,
            urgency=urgency,
            reason="Mock analysis based on task keywords"
        )

        return {
            **result.model_dump(),
            "mode": "mock",
            "usage": {"input_tokens": 0, "output_tokens": 0},
            "estimated_cost_usd": 0.0
        }

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze the task. Return ONLY a JSON object with "
                    "category (study/work/personal/other), "
                    "urgency (low/normal/high), and a short reason."
                )
            },
            {
                "role": "user",
                "content": f"Title: {title}\nDescription: {description}"
            }
        ],
        temperature=0
    )

    
    raw = response.choices[0].message.content

    # Remove Markdown formatting from AI response
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0].strip()

    result = TaskAnalysis.model_validate_json(raw)


    usage = response.usage
    input_tokens = usage.prompt_tokens if usage else 0
    output_tokens = usage.completion_tokens if usage else 0

    return {
        **result.model_dump(),
        "mode": "live",
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        },
        "estimated_cost_usd": None
    }
