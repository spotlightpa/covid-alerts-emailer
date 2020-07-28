import pandas as pd
from typing import List


def stack_df(
    df,
    stackCols: List[str],
    xAxisCol: str,
    *,
    yAxisLabel: str = "value",
    categoryLabel: str = "category",
) -> pd.DataFrame:
    """
    Takes a pandas Dataframe and returns a new dataframe with specified columns stacked on top of each
    other. This is useful for creating multi-series charts with Altair.

    Eg. Data like this:

                  date  total_cases  total_tests
        0   2020-03-08            6            6
        1   2020-03-09           10           10
        2   2020-03-10           12           12

    Is converted to this:
                  date   count    data_type
        0   2020-03-08       6  total_cases
        1   2020-03-09      10  total_cases
        2   2020-03-10      12  total_cases
        0   2020-03-08       6  total_tests
        1   2020-03-09      10  total_tests
        2   2020-03-10      12  total_tests

    Args:
        df (pd.Dataframe): Data to stack.
        stackCols (list): A list of strings that represent the names of columns you wish to stack.
        xAxisCol (str): A column that can act as a dependent variable across all columns specified in stackCols and
            would work as an x axis if the date is charted. Eg. a date or time.
        yAxisLabel (str) OPTIONAL: A way of describing the values in all stackCols. Defaults to 'value'
        categoryLabel (str) OPTIONAL: A way of describing the types of data in the stackCols. Defaults to 'category'

    """
    new_df = pd.DataFrame()
    for col in stackCols:
        df_stack = df[[xAxisCol, col]]
        df_stack.columns = [xAxisCol, yAxisLabel]
        df_stack[categoryLabel] = col
        new_df = new_df.append(df_stack)
    return new_df
