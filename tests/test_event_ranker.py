import pytest
from weekend_fun.event_ranker import rank_events


def test_rank_events():
    events = [
        {
            "title": "Jazz Concert",
            "description": "A night of jazz music",
            "date": "2024-03-15",
            "location": "Jazz Club",
            "url": "http://example.com",
        }
    ]
    interests = ["music", "jazz"]

    ranked_events = rank_events(events, interests)
    assert len(ranked_events) == len(events)
    assert "score" in ranked_events[0]
    assert 0 <= ranked_events[0]["score"] <= 1
