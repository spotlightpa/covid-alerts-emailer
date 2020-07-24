import pandas as pd


def desc_choro(county_name: str, data_type: str) -> str:
    output = (
        f"We can get a better sense of how {county_name} County compares with the rest of Pennsylvania by looking at "
        f"its per capita rate. Over the past two weeks, {county_name} had an average of XXX {data_type} per 100,000 people. "
        f"That means it ranked as having the XXX lowest per capita {data_type} rate among Pennsylvania’s 67 counties over that "
        f"period."
    )
    return output
