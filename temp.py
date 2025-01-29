import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="rajesh.korde@gmail.com",
    to_emails="rajesh.korde@gmail.com",
    subject="Sending with Twilio SendGrid is Fun",
    html_content="<strong>and easy to do anywhere, even with Python</strong>",
)
try:
    sg = SendGridAPIClient(
        api_key="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"
    )
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
