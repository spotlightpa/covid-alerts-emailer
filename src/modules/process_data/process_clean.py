import pandas as pd
from typing import Dict, List
import logging
from src.definitions import DIR_OUTPUT
import numpy as np


def process_clean(
    data: Dict[str, List[Dict[str, str]]], *, save_pickle=False
) -> Dict[str, pd.DataFrame]:
    """
    Takes a dict with values representing types of data (cases, deaths, tests...). Each value is a list of ordered
    dictionaries county-by-county data for that data type.

    This func converts each list of ordered dicts into a pandasDataFrame and formats columnnames and sets datatypes. E

    Args:
        data (Dict[List[Dict[str, str]]]): A dict of lists of ordered dicts.
        save_pickle (bool): Save each dataframe as a pickel in the root directory

    Return:
        A dictionary of pandas dataframes with cleaned data.
    """
    clean_data = {}
    for data_type, data_dict in data.items():
        logging.info(
            f"Cleaning '{data_type}' data and converting to Pandas DataFrame..."
        )
        df = pd.DataFrame(data_dict)
        # df.columns = map(str.lower, df.columns)  # set col names to lowercase
        df = df.rename(columns={"Date": "date"})
        for col in df.columns:
            if "date" in col:
                df["date"] = pd.to_datetime(df["date"])
            else:
                # replace empty cells with 0s
                df[col] = df[col].replace(r"^\s*$", 0, regex=True)
                # coerce any cells that include non-numeric numbers into NaN, datatype is now float
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df = df.replace(np.nan, 0, regex=True)  # replace NaNs with 0s
                # now we've handled potentially invalid input, convert dtype to int
                df[col] = df[col].astype(int)

        # add to payload dict
        clean_data[data_type] = df

        # save pickel
        if save_pickle:
            df.to_pickle(f"{DIR_OUTPUT}/{data_type}.pkl")

    return clean_data
