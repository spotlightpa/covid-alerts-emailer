import altair as alt
import logging
import pandas as pd


def daily_and_avg(
    data_type: str,
    df: pd.DataFrame,
    *,
    line_color: str = "#CC0000",
    bar_color: str = "#F4D2D2",
) -> alt.Chart:
    """
    Creates a bar and line chart.

    Args:
        data_type (str): Data for chart.
        df (pd.DataFrame): pandas dataframe for chart.
        line_color (str) OPTIONAL:  Color for chart line.
        line_color (str) OPTIONAL:  Color for chart bars.

    Return:
        Altair chart instance.
    """
    logging.info("Creating daily and moving avg chart...")
    # legend_title_1 = f"New daily {data_type}"
    # df[legend_title_1] = ""
    # df["7 day average"] = ""
    bars = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="date",
            y="added_since_prev_day",
            # opacity=legend_title_1,
            color=alt.value(bar_color),
        )
    )
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            # shape="7 day average",
            color=alt.value(line_color),
            x=alt.X("date", axis=alt.Axis(title=None)),
            y=alt.Y("moving_avg", axis=alt.Axis(title=None)),
        )
    )
    chart = bars + lines
    chart = chart.configure_point(size=0)  # .properties(width=400, height=600)
    logging.info("...chart created")

    return chart
