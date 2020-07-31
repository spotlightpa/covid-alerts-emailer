from src.covid_email_alerts import main


def test_full_single_county(dauphin_county_dict, dauphin_county):
    """ A full program run using just a single county """
    county_name = dauphin_county["name"]
    custom_subject_line = f"COVID-19 FULL test"
    main(dauphin_county_dict, custom_subject_line=custom_subject_line)
