from definitions import DIR_DATA
from src.modules.helper.encode import encode_str_base64
import altair as alt
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
    chart = alt.Chart(data).mark_bar().encode(x=x, y=y,)
    # chart.show()
    if save_chart:
        export_path = str(DIR_DATA / "chart.svg")
        save(chart, str(export_path))

    svg_str = save(chart, fmt="svg")
    svg_encoded = encode_str_base64(svg_str)
    return svg_encoded
