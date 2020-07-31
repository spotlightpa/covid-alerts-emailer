import json
import pytest
import geopandas
from definitions import (
    DIR_TEMPLATES,
    PATH_COUNTY_LIST,
    DIR_FIXTURES_PA_CLEAN,
    PATH_PA_GEOJSON,
)
import altair as alt
from src.assets.data_index import DATA_INDEX
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from typing import Dict, List, Any
import pandas as pd
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_payload.gen_county_payload import gen_county_payload
from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.compare_counties import compare_counties
from src.modules.process_data.helper.get_neighbors import get_neighbors
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_geo import process_geo
from src.modules.process_data.process_individual_county import process_individual_county


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    # Makes it easier to see pandas DFs when printing to console
    pandas_opts()
    # Enables Spotlight altair theme
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")


@pytest.fixture(scope="session")
def dauphin_county_dict() -> Dict[str, Dict]:
    """
    Returns a dict with a single dict containing county and a special testing mailing ID so that mail is not sent to
    actual subscribers.

    """
    return {
        "42043": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Dauphin County",
        },
    }


@pytest.fixture(scope="session")
def dauphin_county(dauphin_county_dict) -> Dict[str, str]:
    """
    Returns a dict with basic info for Dauphin County, including its name and mailing list ID.
    """
    return dauphin_county_dict["42043"]


@pytest.fixture(scope="session")
def data_clean() -> Dict[str, pd.DataFrame]:
    """
    Creates data_clean, ie. a dict of pandas Dataframes emulating Pa. data that has been fetched and had minimal
    cleaning.
    """
    payload = {}
    for data_type, data_index_dict in DATA_INDEX.items():
        payload[data_type] = pd.read_pickle(DIR_FIXTURES_PA_CLEAN / f"{data_type}.pkl")
    return payload


@pytest.fixture(scope="session")
def county_data(dauphin_county, data_clean) -> Dict[str, pd.DataFrame]:
    """
    Creates county_data, ie. a dict of pandas Dataframes with processed cases, deaths, test
    data for a specific county
    """
    county_name = dauphin_county["name"]
    county_name_clean = county_name.replace(" County", "")
    return process_individual_county(
        data_clean, DATA_INDEX, county_name=county_name_clean
    )


@pytest.fixture(scope="session")
def cases_multi_county_moving_avg_per_cap(data_clean, gdf_processed) -> pd.DataFrame:
    """
    A DataFrame representing a day-by-day comparison of moving avg number of new daily cases, per capita,
    for multiple counties.
    """
    neighbors = get_neighbors("Dauphin", gdf_processed)
    compare_list = ["Dauphin"] + neighbors
    data_clean_cases = data_clean["cases"]
    clean_rules = DATA_INDEX["cases"]["clean_rules"]
    return compare_counties(
        data_clean_cases,
        clean_rules=clean_rules,
        compare_field="moving_avg_per_capita",
        counties=compare_list,
    )


@pytest.fixture(scope="session")
def county_payload(
    dauphin_county, data_clean, county_data, gdf_processed
) -> List[Dict[str, Any]]:
    """
    Creates a list of dicts that represents important payload data for email newsletter.
    """
    county_name_clean = dauphin_county["name"].replace(" County", "")
    return gen_county_payload(
        county_name_clean=county_name_clean,
        data_clean=data_clean,
        county_data=county_data,
        gdf=gdf_processed,
    )


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
def html(dauphin_county, county_payload):
    newsletter_vars = gen_jinja_vars(
        dauphin_county["name"],
        county_payload=county_payload,
        newsletter_browser_link="",
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    return html
