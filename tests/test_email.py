from definitions import (
    DIR_TEMPLATES,
    DIR_TESTS_OUTPUT,
    DIR_FIXTURES,
)
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_html.minify import minify_email_html
from src.modules.helper.condense_whitespace import condense_whitespace
from src.modules.send_email.send_email_list import send_email_list
import random


def test_html_no_white_space(html, dauphin_county):
    html = condense_whitespace(
        html, save_path=DIR_TESTS_OUTPUT / "newsletter-no-white.html"
    )
    email_list_id = dauphin_county["id"]
    county_name = dauphin_county["name"]
    subject = (
        f"COVID-19 Report TEST NO-WHITESPACE: {county_name}, {random.randint(0,999999)}"
    )
    send_email_list(html, email_list_id, subject=subject)


def test_minify_html(html):
    result = minify_email_html(html, DIR_TESTS_OUTPUT / "newsletter-minified.html")
    assert result
    print(result)


def test_gen_html(dauphin_county, county_payload):
    county_name = dauphin_county["name"]
    newsletter_vars = gen_jinja_vars(
        county_name, county_payload=county_payload, newsletter_browser_link=""
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(DIR_TESTS_OUTPUT / "newsletter-test.html", "w") as fout:
        fout.writelines(html)


def test_email_send(html, dauphin_county):
    """
    Test that HTML is successfully generated and email sends without throwing an error.
    """
    email_list_id = dauphin_county["id"]
    county_name = dauphin_county["name"]
    subject = (
        f"COVID-19 Report TEST MINIFIED HTML: {county_name}, {random.randint(0,999999)}"
    )
    send_email_list(html, email_list_id, subject=subject)


def test_email_send_minified_html(minified_html, dauphin_county):
    email_list_id = dauphin_county["id"]
    county_name = dauphin_county["name"]
    # use random number to stop gmail from grouping emails by same subject line
    subject = (
        f"COVID-19 Report TEST MINIFIED HTML: {county_name}, {random.randint(0,999999)}"
    )
    send_email_list(minified_html, email_list_id, subject=subject)
