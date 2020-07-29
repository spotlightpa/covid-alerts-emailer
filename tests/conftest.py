import json
import pytest
import geopandas
from definitions import (
    DIR_FIXTURES,
    DIR_TEMPLATES,
    PATH_COUNTY_LIST,
    AWS_BUCKET,
    AWS_DIR_TEST,
    DIR_FIXTURES_PA_CLEAN,
    PATH_PA_GEOJSON,
)
import altair as alt

from src.assets.data_index import data_index
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.assets.chart_index import chart_index
from typing import Dict, List
import pandas as pd
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.compare_counties import compare_counties
from src.modules.process_data.helper.get_neighbors import get_neighbors
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_geo import process_geo


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    # Makes it easier to see pandas DFs when printing to console
    pandas_opts()


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
def data_clean() -> Dict[str, pd.DataFrame]:
    """
    Creates data_clean, ie. a dict of pandas Dataframes emulating Pa. data that has been fetched and had minimal
    cleaning.
    """
    payload = {}
    for data_type, data_index_dict in data_index.items():
        payload[data_type] = pd.read_pickle(DIR_FIXTURES_PA_CLEAN / f"{data_type}.pkl")
    return payload


@pytest.fixture(scope="session")
def cases_multi_county(data_clean, gdf_processed) -> pd.DataFrame:
    """
    A DataFrame representing a day-by-day comparison of cases data between counties.
    """
    neighbors = get_neighbors("Dauphin", gdf_processed)
    compare_list = ["Dauphin"] + neighbors
    data_clean_cases = data_clean["cases"]
    clean_rules = data_index["cases"]["clean_rules"]
    return compare_counties(
        data_clean_cases,
        clean_rules=clean_rules,
        compare_field="moving_avg_per_capita",
        counties=compare_list,
    )


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
def gdf_raw() -> geopandas.GeoDataFrame:
    """
    Creates an instance of a geopandas geodataframe that is freshly loaded from a pa geojson
    file. The gdf has not been merged with cases, deaths, tests data.
    """
    return process_geo(PATH_PA_GEOJSON)


@pytest.fixture(scope="session")
def gdf_processed(gdf_raw, data_clean) -> geopandas.GeoDataFrame:
    """
    Creates an instance of a geopandas geodataframe with the necessary data to create a map.
    """
    return merge_geo(gdf_raw, data_clean)


@pytest.fixture(scope="session")
def html(county, county_payload):
    newsletter_vars = gen_jinja_vars(
        county["name"], county_payload=county_payload, newsletter_browser_link=""
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    return html
