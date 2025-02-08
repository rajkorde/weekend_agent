from os import getenv
from typing import Any

import openai
from dotenv import load_dotenv

load_dotenv()


def rank_events(
    events: list[dict[str, Any]], interests: list[str]
) -> list[dict[str, Any]]:
    """Rank events based on user interests using OpenAI."""
    openai.api_key = getenv("OPENAI_API_KEY")

    ranked_events = []
    for event in events:
        score = _calculate_interest_score(event, interests)
        ranked_events.append({**event, "score": score})

    return sorted(ranked_events, key=lambda x: x["score"], reverse=True)


def _calculate_interest_score(event: dict[str, Any], interests: list[str]) -> float:
    """Calculate an interest score for an event based on user interests."""
    prompt = f"""
    Event Title: {event["title"]}
    Event Description: {event["description"]}
    User Interests: {", ".join(interests)}
    
    On a scale of 0 to 1, how well does this event match the user's interests?
    Provide only the numerical score.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful event matching assistant.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    try:
        score = float(response.choices[0].message.content.strip())
        return min(max(score, 0), 1)  # Ensure score is between 0 and 1
    except ValueError:
        return 0.0
