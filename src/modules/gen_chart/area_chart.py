import altair as alt
import logging

# from vega_datasets import data as dummy_data
from altair_saver import save
from definitions import DIR_DATA
import pandas as pd
from typing import List
from src.modules.helper.encode import encode_str_base64


def area_chart(
    df: pd.DataFrame,
    x_axis_col,
    y_axis_col,
    *,
    category_col=None,
    save_chart=False,
    fmt="svg",
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
        save_chart (bool) OPTIONAL:  If true, file will be saved. Defaults to false.
        fmt (str): File format to return encoded string in. Defaults to svg.
        domain (list) OPTIONAL:  List of all the categories of data that will be displayed. Defaults to None.
        range_ (list) OPTIONAL:  List of color values for each category. Maps to domain. Defaults to None.

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
            color=alt.Color(category_col, scale=alt.Scale(domain=domain, range=range_)),
        )
    )

    if save_chart:
        export_path = str(DIR_DATA / f"area.{fmt}")
        logging.info(f"Saving file as: {export_path}")
        save(chart, export_path)

    svg_str = save(chart, fmt=fmt)
    svg_encoded = encode_str_base64(svg_str)
    return svg_encoded
