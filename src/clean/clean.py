import pandas as pd
from typing import Dict
import numpy as np


def clean(data: Dict[str, Dict], dataIndex: Dict[str, Dict], county: str):
    """
    Converts an ordered dictionary into a Dict and cleans, parses and filters it based on rules supplied in dataIndex

    Args:
        data (dict): Dictionary of ordered dictionaries that contain data to clean/parse/filter
        dataIndex (dict): Dictionary of dictionaries that includes info about how to handle data.
        county (str): The county to filter the data for.
    """
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
        if clean_rules["addedSincePrevDay"]:
            df["addedSincePrevDay"] = df.total.diff()
            df.iloc[0, 2] = df.iloc[0, 1]  # default first val to same as total
        print(df.dtypes)
        print(key)
        print(df)

    return
