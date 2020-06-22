import altair as alt
from vega_datasets import data
from altair_saver import save

from definitions import DIR_DATA


def daily_and_avg(data):
    data["New daily cases"] = ""
    data["7 day average"] = ""
    bars = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x="date",
            y="added_since_prev_day",
            opacity="New daily cases",
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
        title="New cases per day"
    )
    export_path = str(DIR_DATA / "cases.html")
    chart.save(export_path)
