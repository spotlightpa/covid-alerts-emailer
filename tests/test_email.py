import pytest
from definitions import DIR_TEMPLATES, DIR_TESTS_OUTPUT, PATH_FIXTURE_HTML, DIR_OUTPUT
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_html.minify import minify_email_html
from src.modules.send_email.send_email_list import send_email_list


def test_minify_html():
    with PATH_FIXTURE_HTML.open() as f:
        html = f.read()
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
    try:
        send_email_list(
            html, email_list_id, subject=f"COVID-19 Report TEST: {county_name}"
        )
    except Exception as e:
        pytest.fail(f"Test fail: {e}")
