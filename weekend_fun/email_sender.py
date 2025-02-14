import os

from sendgrid import SendGridAPIClient  # type: ignore
from sendgrid.helpers.mail import Mail, To  # type: ignore

from weekend_fun.event_finder import Event


def send_event_email(to_emails: list[str], events: list[Event]) -> None:
    """Send an email with event recommendations."""

    html_content = _create_email_content(events)
    from_email = os.getenv("FROM_EMAIL")

    try:
        message = Mail(
            from_email=from_email,
            to_emails=[To(email) for email in to_emails],
            subject="Your Weekend Event Recommendations",
            html_content=html_content,
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print(f"Error sending email: {e}")


def _create_email_content(events: list[Event]) -> str:
    """Create HTML content for the email."""
    html = """
    <h1>Your Personalized Weekend Events</h1>
    <p>Here are some events we think you'll enjoy:</p>
    """

    for event in events:
        html += f"""
        <div style="margin-bottom: 20px;">
            <h2>{event.name}</h2>
            <p><strong>Date:</strong> {event.date}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p>{event.description if event.description else ""}</p>
            <p><a href="{event.url}">More Information</a></p>
        </div>
        """

    return html
