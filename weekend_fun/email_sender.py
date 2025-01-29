from os import getenv
from typing import Dict, List

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


def send_event_email(to_email: str, events: List[Dict]) -> None:
    """Send an email with event recommendations."""
    sg = SendGridAPIClient(getenv("SENDGRID_API_KEY"))

    html_content = _create_email_content(events)

    message = Mail(
        from_email=getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject="Your Weekend Event Recommendations",
        html_content=html_content,
    )

    try:
        sg.send(message)
    except Exception as e:
        print(f"Error sending email: {e}")


def _create_email_content(events: List[Dict]) -> str:
    """Create HTML content for the email."""
    html = """
    <h1>Your Personalized Weekend Events</h1>
    <p>Here are some events we think you'll enjoy:</p>
    """

    for event in events[:5]:  # Send top 5 events
        html += f"""
        <div style="margin-bottom: 20px;">
            <h2>{event["title"]}</h2>
            <p><strong>Date:</strong> {event["date"]}</p>
            <p><strong>Location:</strong> {event["location"]}</p>
            <p>{event["description"]}</p>
            <p><a href="{event["url"]}">More Information</a></p>
        </div>
        """

    return html
