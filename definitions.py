"""
This file contains important project variables.
"""
import os
from pathlib import Path

# This sets our root directory as the project directory
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root

# DIRECTORIES
DIR_LOGS = ROOT_DIR / "logs"  # main dir for log-related files
DIR_LOGS_OUTPUT = DIR_LOGS / "output"
DIR_LOGS_CONFIG = DIR_LOGS / "config"
DIR_SRC = ROOT_DIR / "src"
DIR_TESTS = ROOT_DIR / "tests"
DIR_ASSETS = DIR_SRC / "assets"
DIR_DATA = DIR_SRC / "data"
DIR_TEMPLATES = DIR_SRC / "templates"
DIR_FIXTURES = DIR_TESTS / "fixtures"
DIR_TESTS_OUTPUT = DIR_TESTS / "output"

# PATHS
PATH_LOGS_CONFIG = DIR_LOGS_CONFIG / "logging.yaml"
PATH_LOGS_CONFIG_TEST = DIR_LOGS_CONFIG / "logging_test.yaml"
PATH_OUTPUT_HTML = DIR_DATA / "newsletter.html"
PATH_DATA_INDEX = DIR_ASSETS / "data_index.json"
PATH_COUNTY_LIST = DIR_ASSETS / "counties.json"
PATH_PA_GEOJSON = DIR_ASSETS / "pa-county.geojson"
PATH_PA_POP = DIR_ASSETS / "pa-county-pop.csv"
PATH_OUTPUT_GEOJSON = DIR_DATA / "pa-county.json"
