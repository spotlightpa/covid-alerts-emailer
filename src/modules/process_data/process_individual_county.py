import pandas as pd
from typing import Dict, Union
import logging
from src.definitions import DIR_OUTPUT
from pathlib import Path

from src.modules.helper.get_county_pop import get_county_pop


def process_individual_county(
    data: Dict[str, pd.DataFrame],
    data_index: Dict[str, Dict],
    county_name: str,
    *,
    save_pickle: bool = False,
    pickle_save_path: Path = None,
) -> Dict[str, pd.DataFrame]:
    """
    Takes a dict of pandas DataFrames and formats column names, filters based on specific county and processes
    based on provided cleaning rules.

    Args:
        data (dict): Dictionary of ordered dictionaries that contain data to clean/parse/filter
        data_index (dict): Dictionary of dictionaries that includes info about how to handle data.
        county_name (str): The county to filter the data for.
        save_pickle (bool, optional): Saves a pickle of the dataframe. Defaults to false.
        pickle_save_path (Path, optional): Path to save pickle.

    Return:
        A dictionary of pandas dataframes with cleaned data.
    """
    processed_data = {}
    for data_type, df in data.items():

        # process
        logging.info(f"Cleaning and processing '{data_type}' data...")
        clean_rules = data_index[data_type]["clean_rules"]
        df = process_datatype(df, clean_rules=clean_rules, county_name=county_name)

        # optional save
        if save_pickle:
            pickle = f"{data_type}.pkl"
            export_path = (
                DIR_OUTPUT / pickle
                if not pickle_save_path
                else pickle_save_path / pickle
            )
            df.to_pickle(export_path)

        # add to payload dict
        processed_data[data_type] = df
        logging.info(f"...data processed")

    return processed_data


def process_datatype(
    df: pd.DataFrame, *, clean_rules: Dict[str, Union[str, bool]], county_name: str,
) -> pd.DataFrame:
    """
    Takes a pandas DataFrame of a specific datatype and cleans/processes it based on instructions in data_index

    Args:
        df (pd.DataFrame): Dictionary of ordered dictionaries that contain data to clean/parse/filter
        clean_rules (dict): Dictionary that includes info about how to handle data.
        county_name (str): The county to filter the data for.

    Returns:
        pd.DataFrame: A pandas DataFrame with updated data.

    """

    # clean county column name
    df = df.rename(columns={county_name: "total"})
    df = df[["date", "total"]]

    # optional rules
    if clean_rules.get("added_since_prev_day"):
        df["added_since_prev_day"] = df.total.diff()
        df["added_since_prev_day"] = df["added_since_prev_day"].apply(
            lambda x: x if x >= 0 else 0
        )  # default value to 0 if its negative
        df.iloc[0, 2] = df.iloc[0, 1]  # default first val to same as total

    if clean_rules.get("set_first_non_zero_val_to_zero"):
        # If the first value is extreme, we may want to remove it. This rule sets the first
        # non-zero number as a zero.
        target_col = clean_rules["set_first_non_zero_val_to_zero"]
        series_list = df[target_col].to_list()
        first_nonzero_row = next(idx for idx, val in enumerate(series_list) if val > 0)
        df.loc[df.index[first_nonzero_row], target_col] = 0

    if clean_rules.get("total_per_capita"):
        county_pop = get_county_pop(county_name)
        df["total_per_capita"] = (
            df["total"] / county_pop
        ) * 100000  # calculate rate per 100k people

    if clean_rules.get("moving_avg"):
        col_to_avg = clean_rules["moving_avg"]
        df["moving_avg"] = df[col_to_avg].rolling(window=7).mean()
        df["moving_avg"] = df["moving_avg"].fillna(0)

    if clean_rules.get("moving_avg") and clean_rules.get("moving_avg_per_capita"):
        county_pop = get_county_pop(county_name)
        df["moving_avg_per_capita"] = (
            df["moving_avg"] / county_pop
        ) * 100000  # calculate rate per 100k people

    return df
