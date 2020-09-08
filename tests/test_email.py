from src.definitions import DIR_TESTS_OUTPUT

from src.modules.helper.condense_whitespace import condense_whitespace
from src.modules.send_email.send_email_list import send_email_list
import random
import pytest
import requests


def test_send_email_dauphin_no_white_space(dauphin_html, dauphin_info):
    """ Test send_email_list with HTML that has condensed white space. Check your inbox to see that HTML looks as
    expected  """
    dauphin_html = condense_whitespace(
        dauphin_html, save_path=DIR_TESTS_OUTPUT / "newsletter-no-white.html"
    )
    email_list_id = dauphin_info["id"]
    county_name = dauphin_info["name"]
    subject = (
        f"COVID-19 Report TEST NO-WHITESPACE: {county_name}, {random.randint(0,999999)}"
    )
    send_email_list(dauphin_html, email_list_id, subject=subject)


def test_retry_send_email_with_http_error():
    """ Test that send_email_list tries to send multiple times before failing """
    email_list_id = "fake-email-list-id"
    county_name = "Dauphin County"
    html = "<div>A sample piece of HTML for testing purposes</div>"
    subject = (
        f"COVID-19 Report TEST RETRY EMAIL: {county_name}, {random.randint(0,999999)}"
    )
    with pytest.raises(requests.HTTPError):
        send_email_list(html, email_list_id, subject=subject)
