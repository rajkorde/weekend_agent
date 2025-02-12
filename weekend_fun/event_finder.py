import asyncio
import json
import os
from datetime import date
from typing import List, Optional

import requests
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger
from pydantic import BaseModel, Field

from weekend_fun.date_extractor import DateExtracter


class Event(BaseModel):
    name: str = Field(description="Name of the Event")
    date: str = Field(description="Date of the event")
    description: Optional[str] = Field(description="Brief description of the Event")
    location: Optional[str] = Field(description="Location of the event")
    url: Optional[str] = Field(description="URL of the event")


class Events(BaseModel):
    events: list[Event] = Field(default_factory=list, description="List of events")

    @staticmethod
    def serialize(events: list[Event], filename: str = "data/scrapedevents.json"):
        with open(filename, "w") as f:
            json.dump([event.model_dump() for event in events], f, indent=2)

    @staticmethod
    def deserialize(filename: str = "data/scrapedevents.json") -> list[Event]:
        with open(filename, "r") as f:
            data = json.load(f)
        events = [Event.model_validate(event) for event in data]
        return events


class EventExtracter:
    _extract_instructions = """
        You will be given a context as a markdown file that has text extracted from a website that contains a list of events and your job is to extract events from the list in a specific format.

        Read the whole context and find every single event.

        Context: {context}
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        base_llm = ChatOpenAI(model=model_name, max_retries=3)
        self.llm = base_llm.with_structured_output(Events)
        self.chunks = []

    async def extract_events(self, chunks: list[str]) -> list[Event]:
        net_events = []

        async def process_chunk(chunk: str) -> list[Event]:
            events_in_chunk = await self.llm.ainvoke(
                [
                    SystemMessage(
                        content=EventExtracter._extract_instructions.format(
                            context=chunk
                        )
                    )
                ],
            )

            assert events_in_chunk is not None and isinstance(events_in_chunk, Events)
            return events_in_chunk.events

        tasks = [process_chunk(chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)

        net_events = [event for result in results for event in result]
        return net_events


def scrape_website(city: str) -> str:
    urls = _get_urls_for_city(city)
    # TODO: only scrape first url
    return _scrape_and_convert_to_md(urls[0])


def _get_urls_for_city(city: str) -> List[str]:
    """Get the URLs for the specified city from config.json."""
    try:
        with open("config/config.json", "r") as f:
            config = json.load(f)
            return config[city]
    except FileNotFoundError:
        logger.error("Error: config/config.json file not found")
        return []
    except json.JSONDecodeError:
        logger.error("Error: Invalid JSON format in config/config.json")
        return []


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


async def filter_weekend_events(
    events: list[Event], sat: date, sun: date
) -> List[Event]:
    date_extractor = DateExtracter()

    tasks = [date_extractor.get_date_range(event.date) for event in events]
    dates = await asyncio.gather(*tasks)

    filtered_events = []
    for event, event_date in zip(events, dates):
        if event_date and (
            event_date.start_date <= sat <= event_date.end_date
            or event_date.start_date <= sun <= event_date.end_date
        ):
            filtered_events.append(event)

    return filtered_events
