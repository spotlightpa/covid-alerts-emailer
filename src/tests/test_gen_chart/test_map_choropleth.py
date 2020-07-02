import logging
import pytest
from definitions import DIR_TESTS_OUTPUT
from src.modules.gen_chart.map_choropleth import map_choropleth


def test_map_choropleth(gdf):
    """
    Test that choropleth map is generated.
    """
    # logs_config()
    # caplog.set_level(logging.INFO)
    try:
        output_path = DIR_TESTS_OUTPUT / "map.png"
        map_choropleth(gdf, output_path, highlight_polygon="Northumberland")
        logging.info(f"View file: {output_path}")
    except Exception as e:
        pytest.fail(f"Test fail: {e}")
