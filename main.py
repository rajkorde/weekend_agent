import asyncio
from typing import Any, Callable, Coroutine

from dotenv import load_dotenv

from weekend_fun.email_sender import send_event_email
from weekend_fun.event_finder import (
    EventExtracter,
    _filter_weekend_events,
    _get_urls_for_city,
    _scrape_and_convert_to_md,
)

# from weekend_fun.event_ranker import rank_events
from weekend_fun.user_manager import get_user_info
from weekend_fun.utils import (
    cheap_markdown_chunker,
    get_weekend_dates,
    read_from_file,
    write_to_file,
)

# def main():
DEBUG = True
SAVE_TOKENS = True

assert load_dotenv()
user_info = get_user_info()

if SAVE_TOKENS:
    text = read_from_file("scraped.md")
else:
    urls = _get_urls_for_city(user_info["city"])
    text = _scrape_and_convert_to_md(urls[0])

if DEBUG:
    print(f"Scraped length: {len(text)}")
    write_to_file(text)

chunks = cheap_markdown_chunker(text)


def run_async_function(
    async_function: Callable[..., Coroutine[Any, Any, Any]], *args: Any
) -> Any:
    try:
        loop = asyncio.get_event_loop()
        return loop.create_task(
            async_function(*args)
        )  # use create_task if running inside jupyter
    except RuntimeError:
        return asyncio.run(async_function(*args))  # Run normally if no loop is running


future = run_async_function(EventExtracter().extract_events, chunks)
# If running in Jupyter, events will be a Future, so await it
try:
    # Check if running inside an existing event loop (Jupyter)
    loop = asyncio.get_running_loop()
    events = await future  # type: ignore
except RuntimeError:
    events = asyncio.run(future)

# TODO: add retry logic for throttling requests
print(events)


# # write response.content to a file
# with open("response.txt", "wb") as f:
#     f.write(response.content)

# Get weekend dates
weekend_start, weekend_end = get_weekend_dates()


# Find and process events
# events = find_events(user_info["city"], weekend_start, weekend_end)

filtered_events = _filter_weekend_events(events, sat=weekend_start, sun=weekend_end)

# Rank events based on user interests
# ranked_events = rank_events(events, user_info["interests"])

# print(ranked_events)

# Send email with recommendations
send_event_email(to_email=user_info["email"], events=events)

print("Event recommendations have been sent to your email!")


# if __name__ == "__main__":
#     main()
