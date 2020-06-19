import requests


def send_email():
    sender_id = 889752
    list_id = "0334629e-463c-4d89-a931-5bb90c46e34f"
    headers = {"Authorization": f"Bearer {token}"}
    n = 3
    data = {
        "name": f"Test Message #{n}",
        "send_to": {"list_ids": [list_id],},
        "email_config": {
            "subject": f"Test Subject #{n}",
            "html_content": """
                <h1>Hello, World!</h1>
                <p>this is a test message.</p>
                <p>
                    <a href="{{{unsubscribe}}}">Click here to unsubscribe.</a>
                </p>
                <p>lorem ipsum.</p>
            """,
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
