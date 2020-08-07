import altair as alt

# from vega_datasets import data as dummy_data
import pandas as pd
from typing import List


def chart_stacked_area(
    df: pd.DataFrame,
    x_axis_col,
    y_axis_col,
    category_col=None,
    domain: List = None,
    range_: List = None,
) -> str:
    """
    Creates a stacked area chart, returns a string of the chart encoded in base64. Default image format is svg.

    Args:
        df (pd.DataFrame): Data for chart.
        x_axis_col (str): Column to use for x axis.
        y_axis_col (str): Column to use for y axis.
        category_col (str): Column that describes the categories of stacked data. Eg. 'data_types'. Defaults to None.
        domain (list) :  List of all the categories of data that will be displayed. Defaults to None.
        range_ (list) :  List of color values for each category. Maps to domain. Defaults to None.

    Return:
        Str: Base 64 encoded string of SVG chart. For usage in HTML tags. Eg.
        <img alt="My Image" src="data:image/svg+xml;base64,<BASE64STRING>"/>
    """
    chart = (
        alt.Chart(df)
        .mark_area()
        .encode(
            x=x_axis_col,
            y=alt.Y(y_axis_col, stack=True),
            color=alt.Color(
                category_col, scale=alt.Scale(domain=domain, range=range_), legend=None
            ),
        )
    )
    return chart
