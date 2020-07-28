import pandas as pd
from typing import List, Dict

from src.modules.process_data.process_individual_county import process_datatype


def compare_counties(
    df: pd.DataFrame,
    data_index: Dict[str, Dict],
    compare_field: str,
    counties: List[str],
):
    """
    Returns a pandas dataframe that compares multiple counties based on a given field.

    Args:
        df (pd.DataFrame): pandas DataFrame representing statewide data for a particular datatype, eg cases.
        data_index (Dict[str, Dict]): data processing instructions
        compare_field (str): Name of the field in df that counties will be compared by. Eg. 'total cases'
        counties (List[str]): List of strings representing counties to compare
    """
    for county_name in counties:
        clean_rules = data_index[data_type]["clean_rules"]
        df = process_datatype(df, clean_rules=clean_rules, county_name=county_name)
        print(df)
