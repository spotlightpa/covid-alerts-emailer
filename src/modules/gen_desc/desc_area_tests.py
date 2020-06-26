import pandas as pd


def desc_area_tests(data: pd.DataFrame, county: str) -> str:

    output = (
        f"Over the past week, there's been an average of XXX % positive tests to XXX % negative tests in "
        f"{county}. "
    )
    return output
