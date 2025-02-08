import asyncio
import re
from datetime import date, datetime, timedelta
from typing import Any, Callable, Coroutine


def cheap_markdown_chunker(text: str) -> list[str]:
    lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
    section = " "
    sections = []
    for line in lines:
        # split based on section headers in md file
        match = re.match(r"^(#{1,6})\s+(.*)", line)
        if match:
            sections.append(section)
            section = match.group(2).strip()
        else:
            section += f"\n{line}"

    return sections


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


def read_from_file(file_path: str = "scraped.md") -> str:
    content = ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print(f"Error writing to file: {e}")

    return content


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
