import json
from datetime import datetime, timedelta
from pathlib import Path

# from weekend_fun.email_sender import send_event_email
# from weekend_fun.event_finder import find_events
# from weekend_fun.event_ranker import rank_events
from weekend_fun.user_manager import get_user_info


def get_weekend_dates() -> tuple[datetime, datetime]:
    """Get the next weekend's start and end dates."""
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_until_saturday)
    sunday = saturday + timedelta(days=1)
    return saturday, sunday


def main():
    # Get user information
    user_info = get_user_info()

    # Save user info
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / "user_info.json", "w") as f:
        json.dump(user_info, f)

    # Get weekend dates
    weekend_start, weekend_end = get_weekend_dates()

    # Find and process events
    events = find_events(user_info["city"], weekend_start, weekend_end)

    # Rank events based on user interests
    ranked_events = rank_events(events, user_info["interests"])

    print(ranked_events)

    # Send email with recommendations
    # send_event_email(user_info["email"], ranked_events)

    print("Event recommendations have been sent to your email!")


if __name__ == "__main__":
    main()
