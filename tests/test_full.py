from src.covid_email_alerts import main


def test_full_single_county(dauphin_county_dict):
    """ A full program run using just a single county """
    main(dauphin_county_dict)
