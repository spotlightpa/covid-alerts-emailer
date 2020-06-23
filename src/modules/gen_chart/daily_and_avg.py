from definitions import DIR_DATA
from src.modules.helper.encode import encode_str_base64, encode_bytes_as_base64
import altair as alt
from altair_saver import save
import logging
import pandas as pd


def daily_and_avg(
    data_type: str,
    df: pd.DataFrame,
    *,
    fmt: str = "svg",
    save_chart: bool = False,
    line_color: str = "#CC0000",
    bar_color: str = "#F4D2D2",
) -> str:
    """
    Creates a bar and line chart, returns a string of the chart encoded in base64. Default image format is svg.

    Args:
        data_type (str): Data for chart.
        df (pd.DataFrame): pandas dataframe for chart.
        fmt (str): File format to return encoded string in. Defaults to svg.
        save_chart (bool) OPTIONAL:  If true, file will be saved. Defaults to false.
        line_color (str) OPTIONAL:  Color for chart line.
        line_color (str) OPTIONAL:  Color for chart bars.

    Return:
        Str: Base 64 encoded string of SVG chart or base 64 encoded bytes of PNG. For usage in HTML tags. Eg.
        <img alt="My Image" src="data:image/svg+xml;base64,<BASE64STRING>"/>
    """
    logging.info("Creating daily and moving avg chart...")
    legend_title_1 = f"New daily {data_type}"
    df[legend_title_1] = ""
    df["7 day average"] = ""
    bars = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="date",
            y="added_since_prev_day",
            opacity=legend_title_1,
            color=alt.value(bar_color),
        )
    )
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            shape="7 day average",
            color=alt.value(line_color),
            x=alt.X("date", axis=alt.Axis(title=None)),
            y=alt.Y("moving_avg", axis=alt.Axis(title=None)),
        )
    )
    chart = bars + lines
    chart = chart.configure_point(size=0)
    logging.info("...chart created")

    if save_chart:
        logging.info("Saving chart to file...")
        export_path = str(DIR_DATA / f"{data_type}.{fmt}")
        logging.info(f"Saving file as: {export_path}")
        save(chart, export_path)
        logging.info("...saved")

    # Return encoded image file
    chart_saved = save(chart, fmt=fmt)
    if "svg" in fmt:
        chart_encoded = encode_str_base64(chart_saved)
    else:
        chart_encoded = encode_bytes_as_base64(chart_saved)

    return chart_encoded
