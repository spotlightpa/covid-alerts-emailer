import logging
import pytest
from covid_email_alerts.definitions import DIR_TESTS_OUTPUT
from covid_email_alerts.modules.gen_chart.custom_legend import CustomLegend
from covid_email_alerts.modules.gen_chart.multi_line import multi_line
from covid_email_alerts.modules.gen_chart.map_choropleth import map_choropleth
from altair_saver import save

from covid_email_alerts.modules.gen_desc.gen_desc import GenDesc
from covid_email_alerts.modules.helper.stack_df import stack_df


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


def test_multi_line(cases_multi_county_moving_avg_per_cap, gdf_processed):
    counties = [
        col for col in cases_multi_county_moving_avg_per_cap.columns if col != "date"
    ]
    counties = counties[0:5]
    df = stack_df(
        cases_multi_county_moving_avg_per_cap, stack_cols=counties, x_axis_col="date"
    )
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


def test_gen_desc(data_clean, county_data, gdf_processed):
    print("\n", gdf_processed)
    gen_desc = GenDesc("Dauphin", county_data, gdf=gdf_processed)
    result = gen_desc.area_tests()
    print(result)
