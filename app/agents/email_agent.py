import os
import logging
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from pydantic import BaseModel, Field, ValidationError
from agents import Agent, function_tool

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailRequest(BaseModel):
    subject: str = Field(..., description="Email subject line")
    html_body: str = Field(..., description="HTML content of the email")

class EmailResponse(BaseModel):
    status: str = Field(..., description="Result status: 'success' or 'failure'")

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    # Validate input
    try:
        request = EmailRequest(subject=subject, html_body=html_body)
        logger.info("EmailRequest validated: subject='%s'", request.subject)
    except ValidationError as e:
        logger.error("Invalid email request: %s", e)
        return EmailResponse(status="failure").dict()

    # Prepare SendGrid client
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        logger.error("SENDGRID_API_KEY not configured in environment")
        return EmailResponse(status="failure").dict()
    sg = sendgrid.SendGridAPIClient(api_key=api_key)

    # Build email components
    from_email = Email("pramodyasahan.edu@gmail.com")  # Verified sender
    to_email = To("pramodyasahan.edu@gmail.com")        # Recipient
    content = Content("text/html", request.html_body)
    mail = Mail(from_email, to_email, request.subject, content).get()

    # Send email and log response
    try:
        logger.info("Sending email to %s", to_email.email)
        response = sg.client.mail.send.post(request_body=mail)
        logger.info("Email response status: %s", response.status_code)
        if 200 <= response.status_code < 300:
            return EmailResponse(status="success").dict()
        else:
            logger.error("Failed to send email, response body: %s", getattr(response, 'body', ''))
            return EmailResponse(status="failure").dict()
    except Exception as e:
        logger.exception("Exception occurred while sending email: %s", e)
        return EmailResponse(status="failure").dict()

# Agent instructions
INSTRUCTIONS = (
    "You are able to send a nicely formatted HTML email based on a detailed report.\n"
    "You will be provided with a detailed report. You should use your tool to send one email, providing the "
    "report converted into clean, well presented HTML with an appropriate subject line."
)

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
