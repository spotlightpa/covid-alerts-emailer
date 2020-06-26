import pandas as pd


def desc_daily(data: pd.DataFrame, data_type: str, county: str) -> str:

    output = (
        f"Over the past week, there has been a total of XXX new {data_type} in {county}, with a daily average of XXX "
        f"{data_type}."
    )
    return output
