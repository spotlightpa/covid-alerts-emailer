from definitions import DIR_DATA
from src.modules.helper.encode import encode_str_base64
import altair as alt
from altair_saver import save
import logging


def daily_and_avg(
    data_type: str, data, *, fmt: str = "svg", save_chart: bool = False
) -> str:
    """
    Creates a bar and line chart, returns a string of the chart encoded in base64. Default image format is svg.

    Args:
        data (): Data for chart.
        fmt (str): File format to return encoded string in. Defaults to svg.
        save_chart (bool): If true, file will be saved. Defaults to false.

    Return:
        Str: Base 64 encoded string of SVG chart. For usage in HTML tags. Eg.
        <img alt="My Image" src="data:image/svg+xml;base64,<BASE64STRING>"/>
    """
    logging.info("Creating daily and moving avg chart...")
    legend_title_1 = f"New daily {data_type}"
    data[legend_title_1] = ""
    data["7 day average"] = ""
    bars = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x="date",
            y="added_since_prev_day",
            opacity=legend_title_1,
            color=alt.value("#F4D2D2"),
        )
    )
    lines = (
        alt.Chart(data)
        .mark_line()
        .encode(
            shape="7 day average",
            color=alt.value("#CC0000"),
            x=alt.X("date", axis=alt.Axis(title=None)),
            y=alt.Y("moving_avg", axis=alt.Axis(title=None,)),
        )
    )
    chart = bars + lines
    chart = chart.configure_point(size=0, color="red", filled=True).properties(
        title=f"{data_type} per day"
    )

    logging.info("...chart created")
    if save_chart:
        export_path = str(DIR_DATA / f"{data_type}.{fmt}")
        logging.info(f"Saving file as: {export_path}")
        save(chart, export_path)

    svg_str = save(chart, fmt=fmt)
    svg_encoded = encode_str_base64(svg_str)
    return svg_encoded
