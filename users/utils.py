import logging
import uuid

import requests
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from requests.auth import HTTPBasicAuth

PLAYMOBILE_URL = settings.PLAYMOBILE_URL

PLAYMOBILE_AUTH = HTTPBasicAuth(
    username=settings.PLAYMOBILE_LOGIN, password=settings.PLAYMOBILE_PASSWORD
)


def play_mobile_send_sms(recipient: str, text: str):
    # This logic for https://playmobile.uz/ sms provider
    message_id = f"inmall {uuid.uuid4().node}"[:20]
    headers = {
        # "User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", # noqa
        "Content-Type": "application/json"
    }
    originator = "3700"
    payload = {
        "messages": [
            {
                "recipient": recipient,
                "message-id": message_id,
                "sms": {"originator": originator, "content": {"text": text}},
            }
        ]
    }

    try:
        response = requests.post(
            PLAYMOBILE_URL,
            auth=PLAYMOBILE_AUTH,
            json=payload,
            headers=headers,
        )
        return response
    except Exception as e:
        logging.exception(e)


def send_sms(recipient: str, text: str, attempts: int = 1):
    headers = {"Content-Type": "application/json"}
    payload = {
        "messages": [
            {
                "recipient": recipient,
                "message-id": f"inmall {uuid.uuid4().node}"[:20],
                "sms": {"originator": "3700", "content": {"text": text}},
            }
        ]
    }
    response = requests.post(
        PLAYMOBILE_URL,
        auth=PLAYMOBILE_AUTH,
        json=payload,
        headers=headers,
    )
    if response.status_code >= 500:
        logging.error(
            "An error occurred while sending sms, status:{}, text:{}".format(
                response.status_code, response.text
            )
        )
        attempts += 1
        if attempts <= 3:
            logging.info("Send sms failed, attempting:{}".format(attempts))
            return send_sms(recipient, text, attempts + 1)
        return False
    if response.status_code == 200:
        return True
    logging.error(
        "An error occurred while sending sms, status:{}, text:{}".format(
            response.status_code, response.text
        )
    )
    return False


def send_email(email_address: str, subject: str, html_content: str):
    try:
        # Create the email message
        message = EmailMessage(
            subject, html_content, settings.EMAIL_HOST_USER, [email_address]
        )
        # Set content subtype to HTML
        message.content_subtype = "html"
        # Send the email
        message.send()
        return True
    except BadHeaderError as e:
        logging.exception(f"Invalid header found.: {e}")
    except Exception as e:
        logging.exception(f"Failed to send email: {str(e)}")
