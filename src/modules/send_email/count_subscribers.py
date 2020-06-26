import os
import requests
from typing import Dict


def count_subscribers(list_id: str) -> Dict:
    """
    Counts the number of subscribers to a particular SendGrid email newsletter list.
    """
    token = os.environ.get("SENDGRID_API_KEY")
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.sendgrid.com/v3/marketing/lists/{list_id}/contacts/count"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    count_dict = resp.json()
    contact_count = int(count_dict["contact_count"])
    return contact_count
