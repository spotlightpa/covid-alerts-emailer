import json

import pytest
from dotenv import load_dotenv

from definitions import DIR_TEMPLATES, PATH_COUNTY_LIST
from src.modules.gen_html.gen_html import gen_html
from src.modules.send_email.send_email_list import send_email_list
from src.tests.fixtures.newsletter_vars import gen_dummy_template_vars
from assets.data_index import data_index

def test_email_send():
    """
    Test that HTML is successfully generated and email sends.
    """
    with open(PATH_COUNTY_LIST) as f:
        counties = json.load(f)
    county = counties["42043"]["name"]
    email_list_id = counties["42043"]["id"]
    newsletter_vars = gen_dummy_template_vars(county)
    print(newsletter_vars)
    try:
        html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
        send_email_list(html, email_list_id, subject=f"COVID-19 Report: {county}")
    except Exception as e:
        pytest.fail(f"Test fail: {e}")
