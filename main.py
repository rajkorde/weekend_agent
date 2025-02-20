import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger

from weekend_fun.email_sender import send_event_email
from weekend_fun.event_finder import (
    EventExtracter,
    Events,
    filter_weekend_events,
    scrape_website,
)

# from weekend_fun.event_ranker import rank_events
from weekend_fun.event_ranker import EventRanker
from weekend_fun.feature_flag import FeatureFlags
from weekend_fun.user_manager import get_user_info
from weekend_fun.utils import (
    cheap_markdown_chunker,
    get_weekend_dates,
    read_from_file,
    write_to_file,
)


async def main():
    print(os.environ)
    # Setup
    logger.info("Reading in user info and feature flags")
    user_info = get_user_info()
    flags = FeatureFlags.read_feature_flags()

    if not flags.use_docker:
        assert load_dotenv()

    # Scrape website
    logger.info("Scraping websites")
    if flags.scrape:
        text = scrape_website(user_info["city"])
    else:
        text = read_from_file("data/scraped.md")
    logger.info(f"Scraped length: {len(text)}")
    if flags.scrape and flags.save:
        write_to_file(text, "data/scraped.md")

    # Chunk text
    logger.info("Chunking text")
    chunks = cheap_markdown_chunker(text)

    # Extract events
    logger.info("Extracting events")
    if flags.extract:
        # TODO: add tenacity retry logic for throttling requests
        # If running in Jupyter, events will be a Future, so await it
        try:
            # Check if running inside an existing event loop (Jupyter)
            asyncio.get_running_loop()
            events = await EventExtracter().extract_events(chunks)  # noqa # type: ignore
        except RuntimeError:
            events = asyncio.run(EventExtracter().extract_events(chunks))
    else:
        events = Events.deserialize(filename="data/scraped_events.json")
    assert isinstance(events, list)
    logger.info(f"Found total {len(events)} events")

    if flags.extract and flags.save:
        Events.serialize(events, filename="data/scraped_events.json")

    # # write response.content to a file
    # with open("response.txt", "wb") as f:
    #     f.write(response.content)

    # Get weekend dates
    weekend_start, weekend_end = get_weekend_dates()
    if flags.use_test_events:
        weekend_start = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
        weekend_end = datetime.strptime("2025-01-02", "%Y-%m-%d").date()

    # Find and process events
    logger.info("Filtering events")
    if flags.filter:
        # TODO: add tenacity retry logic for throttling requests
        # If running in Jupyter, events will be a Future, so await it
        try:
            # Check if running inside an existing event loop (Jupyter)
            asyncio.get_running_loop()
            events = await filter_weekend_events(events, weekend_start, weekend_end)  # noqa # type: ignore
        except RuntimeError:
            events = asyncio.run(
                filter_weekend_events(events, weekend_start, weekend_end)
            )
        Events.serialize(events, filename="data/filtered_events.json")
    else:
        events = Events.deserialize(filename="data/filtered_events.json")
    logger.info(f"Found {len(events)} events for this weekend")
    if flags.extract and flags.save:
        Events.serialize(events, filename="data/filtered_events.json")

    # Rank events based on user interests
    logger.info("Ranking events")
    if flags.rank:
        try:
            # Check if running inside an existing event loop (Jupyter)
            asyncio.get_running_loop()
            ranked_events = await EventRanker().rank_events(
                events, user_info["interests"]
            )  # noqa # type: ignore
        except RuntimeError:
            ranked_events = asyncio.run(
                EventRanker().rank_events(events, user_info["interests"])
            )
        if flags.save:
            Events.serialize(ranked_events, filename="data/ranked_events.json")
    else:
        ranked_events = Events.deserialize(filename="data/ranked_events.json")
    # print(ranked_events)

    # Send email with recommendations
    logger.info("Sending email")
    if flags.email:
        send_event_email(to_emails=user_info["email"], events=ranked_events)
        logger.info("Email sent")
    else:
        for event in ranked_events:
            logger.debug(f"{event}")


if __name__ == "__main__":
    asyncio.run(main())
