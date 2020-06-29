import json

import pytest
import geopandas
from definitions import DIR_FIXTURES, DIR_TEMPLATES, PATH_COUNTY_LIST
import altair as alt
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.modules.helper.formatters import format_commas
from src.modules.helper.time import est_now_formatted_brief
from assets.data_index import data_index


@pytest.fixture(scope="session")
def county():
    with open(PATH_COUNTY_LIST) as f:
        counties = json.load(f)
    return counties["42043"]


@pytest.fixture(scope="session")
def aws_bucket():
    return {
        "name": "interactives.data.spotlightpa.org",
        "test_dir": "assets/covid-email-alerts/test",
    }


@pytest.fixture(scope="session")
def county_payload(aws_bucket, county):
    county_name = county["name"]
    bucket_name = aws_bucket["name"]
    bucket_dest_dir = aws_bucket["test_dir"]

    payload = []
    for data_type, data_index_dict in data_index.items():
        for chart_dict in data_index_dict["charts"]:
            chart_type = chart_dict["type"]
            payload.append(
                {
                    "title": "",
                    "legend": chart_dict["legend"],
                    "image_path": f"https://{bucket_name}/{bucket_dest_dir}/{county_name}_{data_type}_{chart_type}.png",
                    "description": "Description of chart and stats, blah blah blah",
                }
            )
    return payload


@pytest.fixture(scope="session")
def newsletter_vars(county, county_payload, aws_bucket):
    county_name = county["name"]
    bucket_name = aws_bucket["name"]
    bucket_dest_dir = aws_bucket["test_dir"]

    payload = {
        "stats_pa": {
            "title": "Pennsylvania",
            "stats_items": [
                {"label": "cases", "value": format_commas(10000),},
                {"label": "deaths", "value": format_commas(1000),},
            ],
        },
        "stats_county": {
            "title": f"{county_name}",
            "stats_items": [
                {"label": "cases", "value": format_commas(2000),},
                {"label": "deaths", "value": format_commas(200),},
            ],
        },
        "preview_text": f"Here are the latest stats on cases, deaths, and testing in {county_name}",
        "newsletter_browser_link": f"https://{bucket_name}/{bucket_dest_dir}/newsletter.html",
        "unsubscribe_preferences_link": "{{{unsubscribe_preferences}}}",
        "unsubscribe_link": "{{{unsubscribe}}}",
        "head": {
            "title": f"The latest COVID-19 statistics for {county_name} from Spotlight PA."
        },
        "hero": {
            "title": "COVID-19 Report",
            "tagline": f"The latest COVID-19 statistics for {county_name}.",
            "date": est_now_formatted_brief(),
        },
        "sections": county_payload,
    }
    return payload


@pytest.fixture(scope="session")
def enable_theme():
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")


@pytest.fixture(scope="session")
def gdf(enable_theme):
    gdf = geopandas.read_file(DIR_FIXTURES / "pa_geodata.geojson")
    return gdf


@pytest.fixture(scope="session")
def html(county, newsletter_vars):
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    return html
