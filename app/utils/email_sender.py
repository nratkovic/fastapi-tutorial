from email.message import EmailMessage
from smtplib import SMTP

from ..config import settings


def send_email(content: str, subject: str, mail_to: str):
    # Create email object
    message = EmailMessage()
    message.set_content(content)
    message["Subject"] = subject
    message["From"] = settings.mail_from
    message["To"] = mail_to

    with SMTP(host=settings.mail_server, port=settings.mail_port) as smtp:
        smtp.ehlo()
        # Connect securely to the server with encryption mechanism
        smtp.starttls()
        smtp.login(settings.mail_username, settings.mail_password)
        smtp.send_message(message)


def send_confirmation_email(mail_to: str):
    message = "Hi! Please confirm your registration."
    send_email(message, "Please confirm your registration", mail_to)
