from src.definitions import (
    DIR_TEMPLATES,
    DIR_TESTS_OUTPUT,
)
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_html.minify import minify_email_html
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


def test_gen_html_dauphin(dauphin_info, dauphin_payload, stories_clean):
    county_name = dauphin_info["name"]
    newsletter_vars = gen_jinja_vars(
        county_name,
        county_payload=dauphin_payload,
        newsletter_browser_link="",
        story_promo=stories_clean,
    )
    print("Newsletter vars", newsletter_vars)
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(DIR_TESTS_OUTPUT / "newsletter-test.html", "w") as fout:
        fout.writelines(html)


def test_gen_html_greene(greene_county_dict, greene_payload, stories_clean):
    county_name = greene_county_dict["42059"]["name"]
    newsletter_vars = gen_jinja_vars(
        county_name,
        county_payload=greene_payload,
        newsletter_browser_link="",
        story_promo=stories_clean,
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(DIR_TESTS_OUTPUT / "newsletter-test.html", "w") as fout:
        fout.writelines(html)
