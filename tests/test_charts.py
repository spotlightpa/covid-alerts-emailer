import logging
import pytest
from definitions import DIR_TESTS_OUTPUT
from src.modules.gen_chart.CustomLegend import CustomLegend
from src.modules.gen_chart.multi_line import multi_line
from src.modules.gen_chart.map_choropleth import map_choropleth
from altair_saver import save
from vega_datasets import data
from palettable.colorbrewer.qualitative import Dark2_5
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


def test_gen_custom_legend():
    labels = [
        "dauphin",
        "cumberland",
        "york",
        "lancaster",
    ]
    legend_obj = CustomLegend(labels)
    legend = legend_obj.legend()
    assert len(legend) == 4


def test_gen_custom_legend_limit():
    labels = [
        "dauphin",
        "cumberland",
        "york",
        "lancaster",
    ]
    legend_obj = CustomLegend(labels, limit_labels=2)
    legend = legend_obj.legend()
    print(legend)
    assert len(legend) == 2


def test_multi_line(cases_multi_county, gdf):
    counties = [col for col in cases_multi_county.columns if col != "date"]
    counties = counties[0:5]
    df = stack_df(cases_multi_county, stackCols=counties, xAxisCol="date")
    legend_obj = CustomLegend(counties)
    chart = multi_line(
        df,
        x_axis_col="date",
        y_axis_col="value",
        category_col="category",
        domain=counties,
        range_=legend_obj.colors,
    )
    output_path = DIR_TESTS_OUTPUT / "multiline.png"
    save(chart, str(output_path))
