from datetime import date, datetime, timedelta


def get_weekend_dates() -> tuple[date, date]:
    """Get the next weekend's start and end dates."""
    today = datetime.date(datetime.now())
    days_until_saturday = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_until_saturday)
    sunday = saturday + timedelta(days=1)
    return saturday, sunday


def write_to_file(text: str, file_path: str = "scraped.md") -> None:
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing to file: {e}")
