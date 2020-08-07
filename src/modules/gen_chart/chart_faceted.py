import altair as alt
import numpy as np
from vega_datasets import data
from altair import datum

iris = data.iris()


def chart_faceted(
    df,
    *,
    x_axis_col: str,
    y_axis_col: str,
    category_col: str,
    line_color: str = "#CC0000",
    individual_chart_width: int = 163,
    num_of_cols: int = 3
):
    """
    Creates a wrapped facet chart, similar to facet_wrap from ggplot2

    Args:
        df (pd.DataFrame): Data for chart.
        x_axis_col (str): Column to use for x axis.
        y_axis_col (str): Column to use for y axis.
        category_col (str): Column that describes the categories of stacked data. Eg. 'data_types'. Defaults to None.
        individual_chart_width (int): Width and height of chart
        num_of_cols (int, optional) Number of columns in grid. Defaults to 3.
        line_color (str, optional): Color of lines in each line chart. Defaults to "#CC0000"
    """
    y_axis_domain = [0, df[y_axis_col].max()]
    all_categories = df[
        category_col
    ].unique()  # array of strings to use as your filters and titles

    rows = alt.vconcat(data=df)
    numrows = int(np.ceil(len(all_categories) / num_of_cols))
    pointer = 0
    for _ in range(numrows):

        row = all_categories[pointer : pointer + num_of_cols]
        cols = alt.hconcat()

        for a_chart in row:
            # add your layers here
            # line chart
            line = (
                alt.Chart()
                .mark_line()
                .encode(
                    x=x_axis_col,
                    y=alt.Y(y_axis_col, scale=alt.Scale(domain=y_axis_domain),),
                    color=alt.value(line_color),
                )
                .transform_filter(datum[category_col] == a_chart)
                .properties(
                    title=a_chart.title(),
                    height=individual_chart_width,
                    width=individual_chart_width,
                )
            )

            cols |= line

        rows &= cols
        pointer += num_of_cols
    return rows
