from datetime import datetime, timedelta
from pickle import TRUE

from dotenv import load_dotenv

from weekend_fun.event_finder import (
    EventExtracter,
    _filter_weekend_events,
    _get_urls_for_city,
    _scrape_and_convert_to_md,
)

# from weekend_fun.email_sender import send_event_email
# from weekend_fun.event_ranker import rank_events
from weekend_fun.user_manager import get_user_info
from weekend_fun.utils import get_weekend_dates, write_to_file

# def main():
DEBUG = True

assert load_dotenv()
user_info = get_user_info()

urls = _get_urls_for_city(user_info["city"])
text = _scrape_and_convert_to_md(urls[0])

if DEBUG:
    print(f"Scraped length: {len(text)}")
    write_to_file(text)


events = EventExtracter().extract_events(text)


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
# send_event_email(user_info["email"], ranked_events)

print("Event recommendations have been sent to your email!")


# if __name__ == "__main__":
#     main()
