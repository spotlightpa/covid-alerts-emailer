import pandas as pd
from typing import Dict
import logging
from definitions import DIR_DATA


def process_individual_county(
    data: Dict[str, pd.DataFrame],
    data_index: Dict[str, Dict],
    county: str,
    *,
    save_pickle: bool = False,
) -> Dict[str, pd.DataFrame]:
    """
    Takes a dict of pandas DataFrames and formats column names, filters based on specific county and processes
    based on provided cleaning rules.

    Args:
        data (dict): Dictionary of ordered dictionaries that contain data to clean/parse/filter
        data_index (dict): Dictionary of dictionaries that includes info about how to handle data.
        county (str): The county to filter the data for.
        save_pickle (bool): Saves a pickle of the dataframe

    Return:
        A dictionary of pandas dataframes with cleaned data.
    """
    processed_data = {}
    for data_type, df in data.items():
        logging.info(f"Cleaning and processing '{data_type}' data...")

        # clean county column name
        df = df.rename(columns={county: "total"})
        df = df[["date", "total"]]

        # optional rules
        clean_rules = data_index[data_type]["clean_rules"]
        if clean_rules.get("added_since_prev_day", False):
            df["added_since_prev_day"] = df.total.diff()
            df["added_since_prev_day"] = df["added_since_prev_day"].apply(
                lambda x: x if x >= 0 else 0
            )  # default value to 0 if its negative
            df.iloc[0, 2] = df.iloc[0, 1]  # default first val to same as total

        if clean_rules.get("set_first_non_zero_val_to_zero", False):
            # If the first value is extreme, we may want to remove it. This rule sets the first
            # non-zero number as a zero.
            target_col = clean_rules["set_first_non_zero_val_to_zero"]
            series_list = df[target_col].to_list()
            first_nonzero_row = next(
                idx for idx, val in enumerate(series_list) if val > 0
            )
            df.loc[df.index[first_nonzero_row], target_col] = 0

        if clean_rules.get("moving_avg", False):
            col_to_avg = clean_rules["moving_avg"]
            df["moving_avg"] = df[col_to_avg].rolling(window=7).mean()
            df["moving_avg"] = df["moving_avg"].fillna(0).astype("int64")

        # optional save
        if save_pickle:
            export_path = DIR_DATA / f"{data_type}.pkl"
            df.to_pickle(export_path)

        # add to payload dict
        processed_data[data_type] = df
        logging.info(f"...data processed")

    return processed_data
