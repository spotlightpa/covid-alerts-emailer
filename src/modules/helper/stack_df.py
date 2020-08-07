import pandas as pd
from typing import List


def stack_df(
    df,
    stack_cols: List[str],
    x_axis_col: str,
    *,
    y_axis_label: str = "value",
    category_label: str = "category",
) -> pd.DataFrame:
    """
    Takes a pandas Dataframe and returns a new dataframe with specified columns stacked on top of each
    other. This is useful for creating multi-series charts with Altair.

    Note: This same functionality can be achieved with pd.melt()

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
        stack_cols (list): A list of strings that represent the names of columns you wish to stack.
        x_axis_col (str): A column that can act as a dependent variable across all columns specified in stackCols and
            would work as an x axis if the date is charted. Eg. a date or time.
        y_axis_label (str) OPTIONAL: A way of describing the values in all stackCols. Defaults to 'value'
        category_label (str) OPTIONAL: A way of describing the types of data in the stackCols. Defaults to 'category'

    """
    new_df = pd.DataFrame()
    for col in stack_cols:
        df_stack = df[[x_axis_col, col]]
        df_stack.columns = [x_axis_col, y_axis_label]
        df_stack[category_label] = col
        new_df = new_df.append(df_stack)
    return new_df
