import pandas as pd
from typing import Dict
import numpy as np

from definitions import DIR_DATA


def process(
    data: Dict[str, Dict],
    dataIndex: Dict[str, Dict],
    county: str,
    *,
    save_pickle: bool = False,
) -> Dict[str, pd.DataFrame]:
    """
    Converts an ordered dictionary into a Dict and cleans, parses and filters it based on rules supplied in dataIndex

    Args:
        data (dict): Dictionary of ordered dictionaries that contain data to clean/parse/filter
        dataIndex (dict): Dictionary of dictionaries that includes info about how to handle data.
        county (str): The county to filter the data for.
        save_pickle (bool): Saves a pickle of the dataframe

    Return:
        A dictionary of pandas dataframes with cleaned data.
    """
    clean_data = {}
    county = county.lower()
    for key, item in data.items():
        clean_rules = dataIndex[key]["clean_rules"]
        df = pd.DataFrame(item)
        df.columns = map(str.lower, df.columns)  # set col names to lowercase

        # set types
        df["date"] = pd.to_datetime(df["date"])
        df = df[["date", county]]
        df = df.rename(columns={county: "total"})
        df["total"] = df["total"].replace(r"^\s*$", 0, regex=True)
        df = df.astype({"total": "int64"})

        # optional rules
        if clean_rules.get("added_since_prev_day", False):
            df["added_since_prev_day"] = df.total.diff()
            df.iloc[0, 2] = df.iloc[0, 1]  # default first val to same as total

        if clean_rules.get("moving_avg", False):
            col_to_avg = clean_rules["moving_avg"]
            df["moving_avg"] = df[col_to_avg].rolling(window=7).mean()

        print(key)
        print(df)
        # optional save
        if save_pickle:
            export_path = DIR_DATA / f"{key}.pkl"
            df.to_pickle(export_path)

        # add to payload dict
        clean_data[key] = df

    return clean_data
