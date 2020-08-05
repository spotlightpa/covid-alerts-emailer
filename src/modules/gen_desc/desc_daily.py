import pandas as pd


def desc_daily(county_name: str, data_type: str) -> str:

    output = (
        f"There has been a total of XXX reported {data_type} in {county_name} County since the start of the outbreak. "
        f"Over the past two weeks, the county has had a daily average of XXX new {data_type}. Here’s how its trend looks "
        f"since March:"
    )
    return output
