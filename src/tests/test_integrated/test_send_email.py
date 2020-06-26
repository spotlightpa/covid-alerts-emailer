import pytest

from definitions import DIR_TEMPLATES
from src.modules.gen_html.gen_html import gen_html
from src.modules.send_email.send_email_list import send_email_list
from src.tests.fixtures.newsletter_vars import gen_dummy_template_vars


def test_email_send():
    """
    Test to generate HTML and send email.
    """

    county = "Dauphin"
    newsletter_vars = gen_dummy_template_vars(county)
    email_list_id = "0724edae-40a6-48e6-8330-cc06b3c67ede"
    try:
        html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
        send_email_list(html, email_list_id, subject=f"COVID-19 Report: {county}")
    except Exception as e:
        pytest.fail(f"Test fail: {e}")
