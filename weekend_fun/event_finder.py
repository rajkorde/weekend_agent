from datetime import datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def find_events(city: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Find events for the specified city and date range."""
    # Example websites to scrape
    websites = [
        f"https://www.eventbrite.com/d/{city}/events",
        f"https://www.meetup.com/find/?location={city}",
    ]

    events = []
    for website in websites:
        try:
            events.extend(_scrape_events(website))
        except Exception as e:
            print(f"Error scraping {website}: {e}")

    return _filter_weekend_events(events, start_date, end_date)


def _scrape_events(url: str) -> List[Dict]:
    """Scrape events from a given URL using BeautifulSoup."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Example scraping - adjust selectors based on actual website structure
    events = []
    for event in soup.find_all("div", class_="event-card"):  # Adjust class name
        events.append(
            {
                "title": event.find("h2").text.strip()
                if event.find("h2")
                else "No title",
                "description": event.find("p").text.strip()
                if event.find("p")
                else "No description",
                "date": "2024-03-15",  # You'll need to extract actual date
                "location": event.find("address").text.strip()
                if event.find("address")
                else "No location",
                "url": event.find("a")["href"] if event.find("a") else "#",
            }
        )

    return events


def _filter_weekend_events(
    events: List[Dict], start_date: datetime, end_date: datetime
) -> List[Dict]:
    """Filter events to include only those happening during the specified weekend."""
    return [
        event
        for event in events
        if start_date <= datetime.fromisoformat(event["date"]) <= end_date
    ]
