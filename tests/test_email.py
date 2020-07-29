import pytest
from src.modules.send_email.send_email_list import send_email_list


def test_gen_html(county_payload):
    pass


def test_email_send(html, county):
    """
    Test that HTML is successfully generated and email sends without throwing an error.
    """
    email_list_id = county["id"]
    county_name = county["name"]
    try:
        send_email_list(
            html, email_list_id, subject=f"COVID-19 Report TEST: {county_name}"
        )
    except Exception as e:
        pytest.fail(f"Test fail: {e}")
