import pandas as pd
from typing import Dict


def process_stats(data: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """
    Takes a pandas dataframe and returns the total number of cases, deaths, and tests. It does this by getting the last
    row in each dataframe.
    """
    payload = {}
    for data_type, df in data.items():
        last_row = df.tail(1)
        payload[data_type] = last_row["total"].values[0]

    return payload
