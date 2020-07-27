import json
import pytest
import geopandas
from definitions import (
    DIR_FIXTURES,
    DIR_TEMPLATES,
    PATH_COUNTY_LIST,
    AWS_BUCKET,
    AWS_DIR_TEST,
)
import altair as alt
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.assets.chart_index import chart_index
from typing import Dict, List

from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars


@pytest.fixture(scope="session")
def county() -> Dict:
    """
    Gets basic info for a specific county, like its name and mailing list ID,
    from an index.
    """
    with open(PATH_COUNTY_LIST) as f:
        counties = json.load(f)
    # 42043 = Dauphin County
    return counties["42043"]


@pytest.fixture(scope="session")
def county_payload(county: Dict) -> List[Dict]:
    """
    Creates a list of dicts that represents important payload data for email newsletter.
    """
    county_name = county["name"]
    bucket_name = AWS_BUCKET
    bucket_dest_dir = AWS_DIR_TEST

    payload = []
    for data_type, chart_index_dict in chart_index.items():
        chart_payload = []
        primary_color = chart_index_dict["theme"]["colors"]["primary"]
        secondary_color = chart_index_dict["theme"]["colors"]["secondary"]
        for chart_dict in chart_index_dict["charts"]:
            chart_type = chart_dict["type"]
            chart_payload.append(
                {
                    "title": "",
                    "custom_legend": chart_dict.get("custom_legend"),
                    "image_path": f"https://{bucket_name}/{bucket_dest_dir}/{county_name}_{data_type}_{chart_type}.png",
                    "description": "Description of chart and stats, blah blah blah",
                }
            )
        payload.append(
            {
                "title": f"{data_type.upper()}",
                "charts": chart_payload,
                "colors": {"primary": primary_color, "secondary": secondary_color,},
            }
        )

    return payload


@pytest.fixture(scope="session")
def enable_theme() -> None:
    """
    Enables Spotlight altair theme
    """
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")


@pytest.fixture(scope="session")
def gdf(enable_theme) -> geopandas.GeoDataFrame:
    """
    Creates an instance of a geopandas geodataframe with the necessary data to create a map.
    """
    gdf = geopandas.read_file(DIR_FIXTURES / "pa_geodata.geojson")
    return gdf


@pytest.fixture(scope="session")
def html(county, county_payload):
    newsletter_vars = gen_jinja_vars(
        county["name"], county_payload=county_payload, newsletter_browser_link=""
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    return html
