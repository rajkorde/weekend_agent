import asyncio

from dotenv import load_dotenv
from loguru import logger

from weekend_fun.email_sender import send_event_email
from weekend_fun.event_finder import (
    EventExtracter,
    scrape_website,
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
user_info = get_user_info()
flags = FeatureFlags.read_feature_flags()

# Scrape website
if FeatureFlags.scrape:
    text = scrape_website(user_info["city"])
else:
    text = read_from_file("data/scraped.md")
logger.info(f"Scraped length: {len(text)}")
if FeatureFlags.save:
    write_to_file(text)

# Chunk text
chunks = cheap_markdown_chunker(text)


future = run_async_function(EventExtracter().extract_events, chunks)
# If running in Jupyter, events will be a Future, so await it
try:
    # Check if running inside an existing event loop (Jupyter)
    loop = asyncio.get_running_loop()
    events = await future  # type: ignore
except RuntimeError:
    events = asyncio.run(future)

# TODO: add tenacity retry logic for throttling requests
print(events)


# # write response.content to a file
# with open("response.txt", "wb") as f:
#     f.write(response.content)

# Get weekend dates
weekend_start, weekend_end = get_weekend_dates()


# Find and process events
# events = find_events(user_info["city"], weekend_start, weekend_end)

# filtered_events = _filter_weekend_events(events, sat=weekend_start, sun=weekend_end)

# Rank events based on user interests
# ranked_events = rank_events(events, user_info["interests"])

# print(ranked_events)

# Send email with recommendations
send_event_email(to_email=user_info["email"], events=events)

print("Event recommendations have been sent to your email!")


# if __name__ == "__main__":
#     main()
