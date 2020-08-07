import logging
import pytest
from src.definitions import DIR_TESTS_OUTPUT
from src.modules.gen_chart.chart_faceted import chart_faceted
from src.modules.gen_chart.custom_legend import CustomLegend
from src.modules.gen_chart.chart_multi_line import chart_multi_line
from src.modules.gen_chart.map_choropleth import map_choropleth
from altair_saver import save

from src.modules.gen_desc.gen_desc import GenDesc
from src.modules.helper.stack_df import stack_df


def test_chart_faceted(cases_multi_county_moving_avg_per_cap):
    county_cols = list(cases_multi_county_moving_avg_per_cap.columns)
    county_cols.remove("date")
    df = cases_multi_county_moving_avg_per_cap.melt(
        id_vars=["date"],
        var_name="county",
        value_vars=county_cols,
        value_name="cases_per_capita_moving_avg",
    )
    output_path = DIR_TESTS_OUTPUT / "chart_faceted.png"
    chart = chart_faceted(
        df,
        category_col="county",
        x_axis_col="date",
        y_axis_col="cases_per_capita_moving_avg",
    )
    save(chart, str(output_path))


def test_map_choropleth(gdf_processed):
    """
    Test that choropleth map is generated.
    """
    # logs_config()
    # caplog.set_level(logging.INFO)
    try:
        output_path = DIR_TESTS_OUTPUT / "map.png"
        chart = map_choropleth(
            gdf_processed,
            "cases_added_past_two_weeks_per_capita",
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


def test_gen_custom_legend_title_case():
    labels = [
        "dauphin",
        "cumberland",
        "york",
        "lancaster",
    ]
    legend_obj = CustomLegend(labels)
    legend = legend_obj.legend(title_case=True)
    print(legend)
    print(legend_obj.labels)


def test_multi_line(cases_multi_county_moving_avg_per_cap):
    counties = [
        col for col in cases_multi_county_moving_avg_per_cap.columns if col != "date"
    ]
    counties = counties[0:5]
    df = stack_df(
        cases_multi_county_moving_avg_per_cap, stack_cols=counties, x_axis_col="date"
    )
    legend_obj = CustomLegend(counties)
    chart = chart_multi_line(
        df,
        x_axis_col="date",
        y_axis_col="value",
        category_col="category",
        domain=counties,
        range_=legend_obj.colors,
    )
    output_path = DIR_TESTS_OUTPUT / "multiline.png"
    save(chart, str(output_path))


def test_gen_desc(data_clean, county_data, gdf_processed):
    print("\n", gdf_processed)
    gen_desc = GenDesc("Dauphin", county_data, gdf=gdf_processed)
    result = gen_desc.area_tests()
    print(result)
