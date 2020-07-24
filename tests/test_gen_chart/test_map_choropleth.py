import logging
import pytest
from definitions import DIR_TESTS_OUTPUT
from src.modules.gen_chart.map_choropleth import map_choropleth
from altair_saver import save


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
            highlight_polygon="allegheny",
            legend_title="Testing!",
        )
        save(chart, str(output_path))

        logging.info(f"View file: {output_path}")
    except Exception as e:
        pytest.fail(f"Test fail: {e}")
