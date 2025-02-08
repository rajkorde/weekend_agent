import asyncio
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger

from weekend_fun.email_sender import send_event_email
from weekend_fun.event_finder import (
    EventExtracter,
    scrape_website,
    filter_weekend_events,
    Events
)

# from weekend_fun.event_ranker import rank_events
from weekend_fun.feature_flag import FeatureFlags
from weekend_fun.user_manager import get_user_info
from weekend_fun.utils import (
    cheap_markdown_chunker,
    get_weekend_dates,
    read_from_file,
    run_async_function,
    write_to_file,
)

# def main():

# Setup
assert load_dotenv()
logger.info("Reading in user info and feature flags")
user_info = get_user_info()
flags = FeatureFlags.read_feature_flags()

# Scrape website
logger.info("Scraping websites")
if flags.scrape:
    text = scrape_website(user_info["city"])
else:
    text = read_from_file("data/scraped.md")
logger.info(f"Scraped length: {len(text)}")
if flags.scrape and flags.save:
    write_to_file(text)

# Chunk text
logger.info("Chunking text")
chunks = cheap_markdown_chunker(text)

# Extract events
logger.info("Extracting events")
future = run_async_function(EventExtracter().extract_events, chunks)
if flags.extract:
    # TODO: add tenacity retry logic for throttling requests
    # If running in Jupyter, events will be a Future, so await it
    try:
        # Check if running inside an existing event loop (Jupyter)
        loop = asyncio.get_running_loop()
        events = await future  # type: ignore
    except RuntimeError:
    events = asyncio.run(future)
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
if flags.filter:
    events = filter_weekend_events(events, weekend_start, weekend_end)
    Events.serialize(events, filename="data/filtered_events.json")
else:
    events = Events.deserialize(filename="data/filtered_events.json")
logger.info(f"Found {len(events)} events for this weekend")
if flags.extract and flags.save:
    Events.serialize(events, filename="data/filtered_events.json")

# Rank events based on user interests
# ranked_events = rank_events(events, user_info["interests"])

# print(ranked_events)

# Send email with recommendations
if flags.email:
    send_event_email(to_email=user_info["email"], events=events)
    logger.info("Email sent")
else:
    logger.debug("Final events set")
    logger.debug("Final events set")

# if __name__ == "__main__":
#     main()
