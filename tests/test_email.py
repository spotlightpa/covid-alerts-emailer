from src.definitions import DIR_TESTS_OUTPUT

from src.modules.helper.condense_whitespace import condense_whitespace
from src.modules.send_email.send_email_list import send_email_list
import random


def test_send_email_dauphin_no_white_space(dauphin_html, dauphin_info):
    dauphin_html = condense_whitespace(
        dauphin_html, save_path=DIR_TESTS_OUTPUT / "newsletter-no-white.html"
    )
    email_list_id = dauphin_info["id"]
    county_name = dauphin_info["name"]
    subject = (
        f"COVID-19 Report TEST NO-WHITESPACE: {county_name}, {random.randint(0,999999)}"
    )
    send_email_list(dauphin_html, email_list_id, subject=subject)
