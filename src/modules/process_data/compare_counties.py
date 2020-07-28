import pandas as pd
from typing import List, Dict, Union
from src.modules.process_data.process_individual_county import process_datatype


def compare_counties(
    df: pd.DataFrame,
    clean_rules: Dict[str, Union[str, bool]],
    compare_field: str,
    counties: List[str],
) -> pd.DataFrame:
    """
    Returns a pandas dataframe that compares multiple counties based on a given field.

    Args:
        df (pd.DataFrame): pandas DataFrame representing statewide data for a particular datatype, eg cases.
        clean_rules (dict): Dictionary that includes info about how to handle data.
        compare_field (str): Name of the field in df that counties will be compared by. Eg. 'total cases'
        counties (List[str]): List of strings representing counties to compare

    Return:
        pd.DataFrame: DataFrame with county data represented in each column
    """
    df_payload = pd.DataFrame.empty
    for idx, county_name in enumerate(counties):
        df_processed = process_datatype(
            df, clean_rules=clean_rules, county_name=county_name
        )
        df_processed = df_processed[["date", compare_field]]
        df_processed = df_processed.rename(columns={compare_field: county_name.lower()})
        if idx == 0:
            df_payload = df_processed
        else:
            df_payload = df_payload.merge(
                df_processed, how="left", left_on="date", right_on="date"
            )
    return df_payload
