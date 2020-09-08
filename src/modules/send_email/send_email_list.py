import os
import requests
from retry import retry
import logging


@retry(requests.HTTPError, tries=3, delay=3)
def create_campaign(headers, data):
    url = "https://api.sendgrid.com/v3/marketing/singlesends"
    logging.info("Creating email campaign using SendGrid...")
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    logging.info("...campaign created")
    return resp


@retry(requests.HTTPError, tries=3, delay=3)
def send_campaign(headers, ssid):
    send_url = f"https://api.sendgrid.com/v3/marketing/singlesends/{ssid}/schedule"
    logging.info("Sending email campaign using SendGrid...")
    resp = requests.put(send_url, headers=headers, json={"send_at": "now"})
    resp.raise_for_status()
    logging.info("...campaign sent")
    return resp


def send_email_list(html_content: str, list_id: str, *, subject: str) -> None:
    token = os.environ.get("SENDGRID_API_KEY")
    assert (
        token is not None
    ), "A SendGrid API key needs to be defined as an environment variable."
    sender_id = 889752
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": subject,
        "send_to": {"list_ids": [list_id],},
        "email_config": {
            "subject": subject,
            "html_content": html_content,
            "generate_plain_content": True,
            "suppression_group_id": 13641,
            "sender_id": sender_id,
        },
    }
    resp = create_campaign(headers, data)
    ssid = resp.json()["id"]
    send_campaign(headers, ssid)
