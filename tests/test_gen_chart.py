import logging
import pytest
from definitions import DIR_TESTS_OUTPUT
from src.modules.gen_chart.multi_line import multi_line
from src.modules.gen_chart.map_choropleth import map_choropleth
from altair_saver import save
from vega_datasets import data

from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.helper.stack_df import stack_df


def test_map_choropleth(gdf):
    """
    Test that choropleth map is generated.
    """
    # logs_config()
    # caplog.set_level(logging.INFO)
    try:
        output_path = DIR_TESTS_OUTPUT / "map.png"
        chart = map_choropleth(
            gdf,
            "cases_per_capita",
            highlight_polygon="montour",
            legend_title="Legend title!",
        )
        save(chart, str(output_path))

        logging.info(f"View file: {output_path}")
    except Exception as e:
        pytest.fail(f"Test fail: {e}")


def test_multi_line(cases_multi_county, gdf):
    pandas_opts()
    print(gdf[["NAME", "NEIGHBORS"]])
    print(data.stocks())
    print(cases_multi_county)
    cols = [col for col in cases_multi_county.columns if col != "date"]
    cols = cols[0:5]
    print(cols)
    df = stack_df(cases_multi_county, stackCols=cols, xAxisCol="date")
    chart = multi_line(
        df, x_axis_col="date", y_axis_col="value", category_col="category"
    )
    output_path = DIR_TESTS_OUTPUT / "multiline.png"
    save(chart, str(output_path))
