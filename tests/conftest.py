import pytest
import geopandas
from src.definitions import (
    DIR_TEMPLATES,
    DIR_FIXTURES_PA_CLEAN,
    PATH_PA_GEOJSON,
    AWS_DIR_TEST,
    PATH_FIXTURE_STORIES,
    PATH_FIXTURE_CSV_DEATHS_BAD,
)
import altair as alt
from src.assets.data_index import DATA_INDEX
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from typing import Dict, List, Any
import pandas as pd
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_html.minify import minify_email_html
from src.modules.gen_payload.gen_county_payload import gen_county_payload
from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.compare_counties import compare_counties
from src.modules.helper.get_neighbors import get_neighbors
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_geo import process_geo
from src.modules.process_data.process_individual_county import process_individual_county
from dotenv import load_dotenv
import os
import json
from typing import Dict
import csv

# PYTEST IGNORE
from src.modules.process_data.process_stories import process_stories

# don't send emails during full testing suite runs
collect_ignore_glob = [
    "*test_prod_email.py",
    "*test_email.py",
    "*test_full_with_email.py",
]


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    # Makes it easier to see pandas DFs when printing to console
    pandas_opts()
    load_dotenv()
    # this fixes a strange bug with botocore/moto not recognizing AWS credentials: https://github.com/spulec/moto/issues/1941
    os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get("KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get("SECRET_KEY_ID")
    # Enables Spotlight altair theme
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")


@pytest.fixture(scope="session")
def raw_pa_deaths() -> List[Dict[str, str]]:
    """ Loads a CSV of Pa death data that includes random strings. Returns an ordered dict ready to be cleaned/parsed """
    with open(PATH_FIXTURE_CSV_DEATHS_BAD, "r") as fin:
        reader = csv.DictReader(fin)
        csv_data = [x for x in reader]
    return csv_data


@pytest.fixture(scope="session")
def raw_pa_deaths_with_strings() -> List[Dict[str, str]]:
    """ Loads a CSV of Pa death data that includes random strings. Returns an ordered dict ready to be cleaned/parsed """
    with open(PATH_FIXTURE_CSV_DEATHS_BAD, "r") as fin:
        reader = csv.DictReader(fin)
        csv_data = [x for x in reader]
    return csv_data


# @pytest.fixture(scope="session")
# def fetch_live_data() ->


@pytest.fixture(scope="session")
def multi_county_dict() -> Dict[str, Dict]:
    """
    Returns a dict with multiples dict each containing county name and a special testing mailing ID so that mail is NOT
    sent to actual newsletter subscribers.

    """
    return {
        "42003": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Allegheny County",
        },
        "42053": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Forest County",
        },
        "42049": {"id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95", "name": "Erie County",},
        "42055": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Franklin County",
        },
        "42063": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Indiana County",
        },
        "42069": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Lackawanna County",
        },
        "42083": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "McKean County",
        },
    }


@pytest.fixture(scope="session")
def dauphin_county_dict() -> Dict[str, Dict]:
    """
    Returns a dict with a single dict containing county and a special testing mailing ID so that mail is NOT sent to
    actual subscribers.

    """
    return {
        "42043": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Dauphin County",
        },
    }


@pytest.fixture(scope="session")
def phila_county_dict() -> Dict[str, Dict]:
    """
    Returns a dict with a single dict containing county and a special testing mailing ID so that mail is NOT sent to
    actual subscribers.

    """
    return {
        "42101": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Philadelphia County",
        },
    }


@pytest.fixture(scope="session")
def greene_county_dict() -> Dict[str, Dict]:
    """
    Returns a dict with a single dict containing county and a special testing mailing ID so that mail is NOT sent to
    actual subscribers.

    """
    return {
        "42059": {
            "id": "5a839eb5-d3bc-4f65-9fbe-283c02762a95",
            "name": "Greene County",
        },
    }


@pytest.fixture(scope="session")
def dauphin_info(dauphin_county_dict) -> Dict[str, str]:
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
def dauphin_county_data(dauphin_info, data_clean) -> Dict[str, pd.DataFrame]:
    """
    Creates county_data, ie. a dict of pandas Dataframes with processed cases, deaths, test
    data for Dauphin county
    """
    county_name = dauphin_info["name"]
    county_name_clean = county_name.replace(" County", "")
    return process_individual_county(
        data_clean, DATA_INDEX, county_name=county_name_clean
    )


@pytest.fixture(scope="session")
def greene_county_data(greene_county_dict, data_clean) -> Dict[str, pd.DataFrame]:
    """
    Creates county_data, ie. a dict of pandas Dataframes with processed cases, deaths, test
    data for Greene county
    """
    county_name_clean = greene_county_dict["42059"]["name"].replace(" County", "")
    return process_individual_county(
        data_clean, DATA_INDEX, county_name=county_name_clean
    )


@pytest.fixture(scope="session")
def greene_payload(
    greene_county_dict, data_clean, greene_county_data, gdf_processed
) -> List[Dict[str, Any]]:
    """
    Creates a list of dicts that represents important payload data for email newsletter.
    """
    county_name_clean = greene_county_dict["42059"]["name"].replace(" County", "")
    # Note, we use AWS_TESTING_DIR so that assets are uploaded there rather than in the production
    # directory of bucket
    return gen_county_payload(
        county_name_clean=county_name_clean,
        data_clean=data_clean,
        county_data=greene_county_data,
        gdf=gdf_processed,
        aws_dir=AWS_DIR_TEST,
    )


@pytest.fixture(scope="session")
def dauphin_payload(
    dauphin_info, data_clean, dauphin_county_data, gdf_processed
) -> List[Dict[str, Any]]:
    """
    Creates a list of dicts that represents important payload data for email newsletter.
    """
    county_name_clean = dauphin_info["name"].replace(" County", "")
    # Note, we use AWS_TESTING_DIR so that assets are uploaded there rather than in the production
    # directory of bucket
    return gen_county_payload(
        county_name_clean=county_name_clean,
        data_clean=data_clean,
        county_data=dauphin_county_data,
        gdf=gdf_processed,
        aws_dir=AWS_DIR_TEST,
    )


@pytest.fixture(scope="session")
def dauphin_html(dauphin_info, dauphin_payload, stories_clean):
    newsletter_vars = gen_jinja_vars(
        dauphin_info["name"],
        county_payload=dauphin_payload,
        newsletter_browser_link="",  # not needed for testing purposes so we can leave empty
        story_promo=stories_clean,
    )
    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    return html


@pytest.fixture(scope="session")
def dauphin_minif_html(dauphin_html) -> str:
    """ Returns minified HTML"""
    return minify_email_html(dauphin_html, include_comments=True)


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
def dauphin_region_cases_moving_avg_per_cap(data_clean, gdf_processed) -> pd.DataFrame:
    """
    A DataFrame representing a day-by-day comparison of moving avg number of new daily cases, per capita,
    for Dauphin and neighboring counties.
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
def greene_region_deaths_moving_avg_per_cap(data_clean, gdf_processed) -> pd.DataFrame:
    """
    A DataFrame representing a day-by-day comparison of moving avg number of new daily cases, per capita,
    for Dauphin and neighboring counties.
    """
    neighbors = get_neighbors("Greene", gdf_processed)
    compare_list = ["Greene"] + neighbors
    data_clean_deaths = data_clean["deaths"]
    clean_rules = DATA_INDEX["deaths"]["clean_rules"]
    return compare_counties(
        data_clean_deaths,
        clean_rules=clean_rules,
        compare_field="moving_avg_per_capita",
        counties=compare_list,
    )


@pytest.fixture(scope="session")
def stories_raw() -> List[Dict[str, str]]:
    """ Spotlight PA stories copied from summary feed"""
    with open(PATH_FIXTURE_STORIES, "r") as fin:
        stories = fin.read()
    return json.loads(stories)


@pytest.fixture(scope="session")
def stories_clean(stories_raw) -> List[Dict[str, str]]:
    """ Spotlight PA stories cleaned and filtered """
    return process_stories(stories_raw)
