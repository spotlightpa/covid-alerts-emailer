import pytest

from definitions import DIR_TEMPLATES, DIR_TESTS_OUTPUT
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.send_email.send_email_list import send_email_list


def test_gen_html(county, county_payload):
    county_name = county["name"]
    newsletter_vars = gen_jinja_vars(
        county_name, county_payload=county_payload, newsletter_browser_link=""
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(DIR_TESTS_OUTPUT / "newsletter-test.html", "w") as fout:
        fout.writelines(html)


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
