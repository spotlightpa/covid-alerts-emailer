from src.covid_email_alerts import main
import random


def test_full_single_county(dauphin_county_dict, dauphin_county):
    """ A full program run using just a single county """
    county_name = dauphin_county["name"]
    subject = (
        f"COVID-19 Report FULL-RUN TEST: {county_name}, {random.randint(0,999999)}"
    )
    main(dauphin_county_dict, custom_subject_line=subject)
