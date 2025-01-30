import json
import os
from typing import List, Optional

import requests
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str = Field(description="Name of the Event")
    date: str = Field(description="Date of the event")
    description: Optional[str] = Field(description="Brief description of the Event")
    location: Optional[str] = Field(description="Location of the event")
    url: Optional[str] = Field(description="URL of the event")


class Events(BaseModel):
    events: list[Event] = Field(default_factory=list, description="List of events")


class EventExtracter:
    _extract_instructions = """
        You will be given a context as a markdown file that has text extracted from a website that contains a list of events and your job is to extract events from the list in a specific format. 

        Context: {context}
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        base_llm = ChatOpenAI(model=model_name)
        self.llm = base_llm.with_structured_output(Events)

    def extract_events(self, content: str) -> list[Event]:
        event_list = self.llm.invoke(
            [
                SystemMessage(
                    content=EventExtracter._extract_instructions.format(context=content)
                )
            ]
        )
        assert isinstance(event_list, Events)
        return event_list.events if event_list.events else []


def _get_urls_for_city(city: str) -> List[str]:
    """Get the URLs for the specified city from config.json."""
    try:
        with open("data/config.json", "r") as f:
            config = json.load(f)
            return config[city]
    except FileNotFoundError:
        print("Error: data/config.json file not found")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data/config.json")
        return []


# def find_events(city: str, start_date: datetime, end_date: datetime) -> List[Dict]:
#     """Find events for the specified city and date range."""
#     # Example websites to scrape
#     websites = [
#         f"https://www.eventbrite.com/d/{city}/events",
#         f"https://www.meetup.com/find/?location={city}",
#     ]

#     events = []
#     for website in websites:
#         try:
#             events.extend(_scrape_events(website))
#         except Exception as e:
#             print(f"Error scraping {website}: {e}")

#     return _filter_weekend_events(events, start_date, end_date)


def _scrape_and_convert_to_md(url: str) -> str:
    jina_url = "https://r.jina.ai/"

    new_url = jina_url + url
    response = requests.get(
        new_url, {"Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"}
    )

    if response.status_code == 200:
        result = response.content.decode("utf-8", errors="ignore")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        result = ""
    return result


# def _scrape_events(url: str) -> List[Dict]:
#     """Scrape events from a given URL using BeautifulSoup."""
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Example scraping - adjust selectors based on actual website structure
#     events = []
#     for event in soup.find_all("div", class_="event-card"):  # Adjust class name
#         events.append(
#             {
#                 "title": event.find("h2").text.strip()
#                 if event.find("h2")
#                 else "No title",
#                 "description": event.find("p").text.strip()
#                 if event.find("p")
#                 else "No description",
#                 "date": "2024-03-15",  # You'll need to extract actual date
#                 "location": event.find("address").text.strip()
#                 if event.find("address")
#                 else "No location",
#                 "url": event.find("a")["href"] if event.find("a") else "#",
#             }
#         )

#     return events


# def _filter_weekend_events(
#     events: List[Dict], start_date: datetime, end_date: datetime
# ) -> List[Dict]:
#     """Filter events to include only those happening during the specified weekend."""
#     return [
#         event
#         for event in events
#         if start_date <= datetime.fromisoformat(event["date"]) <= end_date
#     ]
