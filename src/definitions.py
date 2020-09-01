"""
This file contains important project variables.
"""
import os
from pathlib import Path
from src.modules.helper.time import est_now_iso


# This sets our root directory as the project directory
ROOT_DIR = (
    Path(os.path.dirname(os.path.abspath(__file__))) / ".."
)  # This is your Project Root

# DIRECTORIES
DIR_LOGS = ROOT_DIR / "logs"  # main dir for log-related files
DIR_LOGS_OUTPUT = DIR_LOGS / "output"
DIR_LOGS_CONFIG = DIR_LOGS / "config"
DIR_SRC = ROOT_DIR / "src"
DIR_TESTS = ROOT_DIR / "tests"
DIR_ASSETS = DIR_SRC / "assets"
DIR_OUTPUT = DIR_SRC / "output"
DIR_TEMPLATES = DIR_SRC / "templates"
DIR_FIXTURES = DIR_TESTS / "fixtures"
DIR_TESTS_OUTPUT = DIR_TESTS / "output"
DIR_FIXTURES_PA_CLEAN = DIR_FIXTURES / "pa_cleaned"

# PATHS
PATH_LOGS_CONFIG = DIR_LOGS_CONFIG / "logging.yaml"
PATH_LOGS_CONFIG_TEST = DIR_LOGS_CONFIG / "logging_test.yaml"
PATH_DATA_INDEX = DIR_ASSETS / "data_index.json"
PATH_COUNTY_LIST = DIR_ASSETS / "counties.json"
PATH_PA_GEOJSON = DIR_ASSETS / "pa-county.geojson"
PATH_PA_POP = DIR_ASSETS / "pa-county-pop.csv"
PATH_OUTPUT_GEOJSON = DIR_OUTPUT / "pa-county.json"
PATH_FIXTURE_HTML = DIR_FIXTURES / "html/newsletter_dauphin.html"
PATH_FIXTURE_STORIES = DIR_FIXTURES / "stories/stories.json"
PATH_FIXTURE_CSV_DEATHS_BAD = DIR_FIXTURES / "csvs/pa-deaths__with-strings.csv"

# FETCH DATA
FETCH_DIR_URL = (
    "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
)

# AWS
AWS_BUCKET = "interactives.data.spotlightpa.org"
AWS_DIR = f"2020/covid-email-alerts/assets/{est_now_iso()}"
AWS_DIR_TEST = "2020/covid-email-alerts/assets/tests"
