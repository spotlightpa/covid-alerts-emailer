import pandas as pd
from typing import Dict
import logging


def process_clean(data: Dict[str, Dict],) -> Dict[str, pd.DataFrame]:
    """
    Takes a dict of ordered dictionaries of county data, converts each one into a pandas DataFrame and formats column
    names and sets datatypes.

    Args:
        data (Dict[str, Dict]): A dict of ordered dictionaries.

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
        print(df.info())
        for col in df.columns:
            if "date" in col:
                df["date"] = pd.to_datetime(df["date"])
            else:
                df[col] = df[col].replace(r"^\s*$", 0, regex=True)
                df[col] = df[col].astype("int")

        # add to payload dict
        clean_data[data_type] = df

    return clean_data
