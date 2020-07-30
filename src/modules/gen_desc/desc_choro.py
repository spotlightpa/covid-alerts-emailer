import pandas as pd


def desc_choro(county_name_clean: str, data_type: str) -> str:
    output = (
        f"Over the past two weeks, {county_name_clean} County had an average of XXX {data_type} per 100,000 people. "
        f"That means it ranked as having the XXX lowest per capita {data_type} rate among Pennsylvania’s 67 counties over that "
        f"time. Here's how {county_name_clean} compares to its four most populous neighbors:"
    )
    return output
