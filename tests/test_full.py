from src.covid_email_alerts import main
import random

from src.definitions import AWS_DIR_TEST


def test_full_dauphin_county(dauphin_county_dict):
    """ A full program run using just a single county """
    county_name = dauphin_county_dict["42043"]["name"]
    subject = (
        f"COVID-19 Report FULL-RUN TEST: {county_name}, {random.randint(0,999999)}"
    )
    main(
        dauphin_county_dict,
        custom_subject_line=subject,
        aws_dir=AWS_DIR_TEST,
        email_send=True,
    )


def test_full_phila_county(phila_county_dict):
    """ A full program run using just a single county """
    county_name = phila_county_dict["42101"]["name"]
    subject = (
        f"COVID-19 Report FULL-RUN TEST: {county_name}, {random.randint(0,999999)}"
    )
    main(
        phila_county_dict,
        custom_subject_line=subject,
        aws_dir=AWS_DIR_TEST,
        email_send=False,
    )


def test_full_greene_county(greene_county_dict):
    """ A full program run using just a single county """
    county_name = greene_county_dict["42059"]["name"]
    subject = (
        f"COVID-19 Report FULL-RUN TEST: {county_name}, {random.randint(0,999999)}"
    )
    main(
        greene_county_dict,
        custom_subject_line=subject,
        aws_dir=AWS_DIR_TEST,
        email_send=True,
    )


def test_full_multi_county(multi_county_dict):
    subject = f"COVID-19 Report FULL-RUN MULTI-COUNTY TEST: {random.randint(0,999999)}"
    main(
        multi_county_dict,
        custom_subject_line=subject,
        aws_dir=AWS_DIR_TEST,
        email_send=True,
    )
