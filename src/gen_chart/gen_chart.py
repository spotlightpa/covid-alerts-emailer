from definitions import DIR_DATA
import os
from definitions import DIR_DATA, PATH_OUTPUT_HTML
from src.helper.encode import encode_str_base64
from src.init.init_program import init_program
import altair as alt
from vega_datasets import data
from altair_saver import save


def gen_chart(data, *, x: str, y: str, save_chart: bool = False) -> str:
    """
    Creates an SVG chart, encoded in base64.

    Args:
        data (): Data for chart.
        save_chart (bool): If true, file will be saved. Defaults to false.

    Return:
        Str. Base 64 encoded string of SVG chart. For usage in HTML tags. Eg.
        <img alt="My Image" src="data:image/svg+xml;base64,<BASE64STRING>"/>
    """
    chart = alt.Chart(data).mark_point().encode(x=x, y=y, color="Origin",)
    # chart.show()
    if save_chart:
        export_path = str(DIR_DATA / "chart.svg")
        save(chart, str(export_path))

    svg_str = save(chart, fmt="svg")
    svg_encoded = encode_str_base64(svg_str)
    return svg_encoded
