from src.covid_email_alerts import main


def test_full(counties_dict1):
    """ Full program run using a select list of counties"""
    main(counties_dict1)


def test_full_no_emails(counties_dict1):
    """ Full program run using a select list of counties but without sending email"""
    main(counties_dict1, email_send=False)


def test_full_single_county(dauphin_county_dict):
    """ A full program run using just a single county """
    main(dauphin_county_dict)
