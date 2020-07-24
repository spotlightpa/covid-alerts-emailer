import os
import requests
import logging


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
    url = "https://api.sendgrid.com/v3/marketing/singlesends"
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    ssid = resp.json()["id"]
    send_url = f"https://api.sendgrid.com/v3/marketing/singlesends/{ssid}/schedule"
    resp = requests.put(send_url, headers=headers, json={"send_at": "now"})
    resp.raise_for_status()
