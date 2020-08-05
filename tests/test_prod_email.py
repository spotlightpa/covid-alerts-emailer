import pytest

from src.covid_email_alerts import main
from src.definitions import AWS_DIR_TEST


def test_full_single_county():
    """
    A program run to a single county on the actual production SendGrid mailing list

    WARNING: Be careful about running this function unless you really intend to send out
    an actual blast to all subscribers on this list. This module should be ignored in conftest.py
    """
    dauphin_county_dict = {
        "42007": {
            "id": "3bd8378c-3183-445e-bffb-278e4af2c09c",
            "name": "Beaver County",
        },
    }
    main(dauphin_county_dict, aws_dir=AWS_DIR_TEST)
